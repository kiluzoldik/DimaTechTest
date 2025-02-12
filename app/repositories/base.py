from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, IntegrityError

from app.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


class BaseRepository:
    model = None
    mapper = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(object) for object in result.scalars().all()]
        
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        try:
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
            
    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError:
            raise ObjectAlreadyExistsException
        
        return result.scalar_one()
    
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning()
        )
        try:
            await self.session.execute(query)
        except NoResultFound:
            raise ObjectNotFoundException
        
    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        try:
            await self.session.execute(delete_stmt)
        except NoResultFound:
            raise ObjectNotFoundException