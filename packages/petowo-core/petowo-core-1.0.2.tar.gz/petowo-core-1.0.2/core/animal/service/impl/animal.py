import logging
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.animal.repository.animal import IAnimalRepository
from core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate, \
    AnimalSchemaDelete
from core.animal.service.animal import IAnimalService
from core.show.repository.show import IShowRepository
from core.show.schema.animalshow import AnimalShowSchema
from core.show.schema.show import ShowStatus
from core.show.service.animalshow import IAnimalShowService
from core.utils.exceptions import NotFoundRepoError, DeleteAnimalStartedShowError
from core.utils.types import ID


class AnimalService(IAnimalService):
    animal_repo: IAnimalRepository
    animalshow_service: IAnimalShowService
    show_repo: IShowRepository

    def __init__(self, animal_repo: IAnimalRepository, animalshow_service: IAnimalShowService,
                 show_repo: IShowRepository):
        self.animal_repo = animal_repo
        self.animalshow_service = animalshow_service
        self.show_repo = show_repo

    def get_animal_registration_records(self, animal_id: ID) -> List[AnimalShowSchema]:
        try:
            records = self.animalshow_service.get_by_animal_id(animal_id)
        except NotFoundRepoError:
            return []
        return records

    def delete(self, animal_id: ID) -> AnimalSchemaDelete:
        logging.info(f'delete animal id={animal_id.value}')

        if not (animal_registration_records := self.get_animal_registration_records(animal_id)):
            self.animal_repo.delete(animal_id.value)
            logging.info(f'success delete animal id={animal_id.value}')
            return AnimalSchemaDelete(id=animal_id)

        shows = []
        for record in animal_registration_records:
            cur_show = self.show_repo.get_by_id(record.show_id.value)
            if cur_show.status == ShowStatus.started:
                logging.info(f'error delete animal id={animal_id.value}: show status is started')
                raise DeleteAnimalStartedShowError(animal_id=animal_id)
            shows.append(cur_show)

        for i, show in enumerate(shows):
            self.animalshow_service.archive(animal_registration_records[i].id)

        self.animal_repo.delete(animal_id.value)
        return AnimalSchemaDelete(id=animal_id)

    def create(self, create_animal: AnimalSchemaCreate) -> AnimalSchema:
        logging.info(f'create animal (user_id={create_animal.user_id.value})')
        new_animal = AnimalSchema.from_create(create_animal)
        return self.animal_repo.create(new_animal)

    def update(self, update_animal: AnimalSchemaUpdate) -> AnimalSchema:
        logging.info(f'update animal={update_animal.id.value}')
        cur_animal = self.animal_repo.get_by_id(update_animal.id.value)
        cur_animal = cur_animal.from_update(update_animal)
        return self.animal_repo.update(cur_animal)

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[AnimalSchema]:
        logging.info(f'get all animals skip={skip}, limit={limit}')
        return self.animal_repo.get_all(skip, limit)

    def get_by_user_id(self, user_id: ID) -> List[AnimalSchema]:
        logging.info(f'get animals by user_id={user_id.value}')
        return self.animal_repo.get_by_user_id(user_id.value)

    def get_by_id(self, animal_id: ID) -> AnimalSchema:
        logging.info(f'get animal by id={animal_id.value}')
        return self.animal_repo.get_by_id(animal_id.value)
