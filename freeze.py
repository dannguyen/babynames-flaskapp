from flask_frozen import Freezer
from app import app
from data_scripts.settings import get_all_names_by_sex

freezer = Freezer(app)


@freezer.register_generator
def sex_name():
    for sex, names in get_all_names_by_sex().items():
        for name in names:
            yield {'sex': sex, 'name': name}



if __name__ == '__main__':
    freezer.freeze()
