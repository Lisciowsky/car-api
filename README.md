# Car rest api
*Contanerized Django RestApi*
<br></br>
## Deployment, dependencies
```
git clone https://github.com/Lisciowsky/car-api && cd car-api
cp .env.example .env
docker-compose up --build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
```
you check it out in http://localhost

## Documentation
**car_collection.json** and **car_environment.json** provided as a api documentation