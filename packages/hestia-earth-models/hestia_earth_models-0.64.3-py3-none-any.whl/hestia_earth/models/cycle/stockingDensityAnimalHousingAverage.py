from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_primary_product

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.blank_node import get_lookup_value
from hestia_earth.models.utils.practice import _new_practice
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "products": [{
            "@type": "Product",
            "primary": "True",
            "term.termType": "liveAnimal"
        }]
    }
}
RETURNS = {
    "Practice": [{
        "value": ""
    }]
}
LOOKUPS = {
    "liveAnimal": "stockingDensityAnimalHousing"
}
TERM_ID = 'stockingDensityAnimalHousingAverage'


def _practice(value: float):
    practice = _new_practice(TERM_ID)
    practice['value'] = [round(value, 7)]
    return practice


def _should_run(cycle: dict):
    product = find_primary_product(cycle)
    is_live_animal_product = (product or {}).get('term', {}).get('termType') == TermTermType.LIVEANIMAL.value

    lookup_value = get_lookup_value((product or {}).get('term', {}), LOOKUPS['liveAnimal'])

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    is_live_animal_product=is_live_animal_product,
                    lookup_value=lookup_value)

    should_run = all([is_live_animal_product > 0, lookup_value is not None])
    logShouldRun(cycle, MODEL, TERM_ID, should_run)
    return should_run, lookup_value


def run(cycle: dict):
    should_run, lookup_value = _should_run(cycle)
    return _practice(lookup_value) if should_run else []
