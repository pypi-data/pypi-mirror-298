import logging
from typing import List

from core.show.repository.animalshow import IAnimalShowRepository
from core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from core.show.service.animalshow import IAnimalShowService
from core.utils.exceptions import AnimalShowServiceError
from core.utils.types import ID


class AnimalShowService(IAnimalShowService):
    animalshow_repo: IAnimalShowRepository

    def __init__(self, animalshow_repo: IAnimalShowRepository):
        self.animalshow_repo = animalshow_repo

    def create(self, animalshow_create: AnimalShowSchemaCreate) -> AnimalShowSchema:
        logging.info(f'create animalshow')
        new_animalshow = AnimalShowSchema.from_create(animalshow_create)
        return self.animalshow_repo.create(new_animalshow)

    def archive(self, animalshow_id: ID) -> AnimalShowSchema:
        logging.info(f'archive animalshow id={animalshow_id.value}')
        cur_animalshow = self.animalshow_repo.get_by_id(animalshow_id.value)
        cur_animalshow.is_archived = True
        return self.animalshow_repo.update(cur_animalshow)

    def delete(self, animalshow_id: ID) -> AnimalShowSchemaDeleted:
        logging.info(f'delete animalshow id={animalshow_id.value}')
        self.animalshow_repo.delete(animalshow_id.value)
        return AnimalShowSchemaDeleted(id=animalshow_id)
    
    def get_by_id(self, id: ID) -> AnimalShowSchema:
        logging.info(f'get animalshow by id={id.value}')
        return self.animalshow_repo.get_by_id(id.value)
    
    def get_by_animal_id(self, animal_id: ID) -> List[AnimalShowSchema]:
        logging.info(f'get animalshows by animal_id={animal_id.value}')
        return self.animalshow_repo.get_by_animal_id(animal_id.value)

    def get_by_show_id(self, show_id: ID) -> List[AnimalShowSchema]:
        logging.info(f'get animalshows by show_id={show_id.value}')
        return self.animalshow_repo.get_by_show_id(show_id.value)

    def get_by_animal_show_id(self, animal_id: ID, show_id: ID) -> AnimalShowSchema:
        logging.info(f'get animalshows animal_id={animal_id.value} show_id={show_id.value}')
        res = self.animalshow_repo.get_by_animal_show_id(animal_id.value, show_id.value)
        if len(res) > 1:
            logging.warning(f'got duplicate animalshow animal_id={animal_id.value} show_id={show_id.value}')
            raise AnimalShowServiceError(detail='More than one animalshow record')
        return res[0]
