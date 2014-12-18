pybabel extract -F ./babel.cfg -o ./locale/messages.pot ./

pybabel update -l es_ES -d ./locale -i ./locale/messages.pot
pybabel update -l en_US -d ./locale -i ./locale/messages.pot


