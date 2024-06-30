# Francis Tech Test

### Setting up the project

This project uses Makefile to handle setting up and running

You can run `make help` to see a list of available commands

To setup this project you should start with `make setup` which will install a virtualenv
and apply migrations

If you see errors with database tables missing on postgres you may have forgotten to run
`make setup` - to apply these migrations manually run `make alembic-migrate`

### Running the code

This code can be ran locally or with docker

There's some related infrastructure (e.g postgres) which will always be ran with Docker

To run locally run `make run` - you can then visit http://localhost:8000/docs

To run in docker run `make run-docker` - then visit http://localhost:8130/docs

### Running tests

`make test`

### Contributing

This repo uses pre-commit for linting -
you should run `pre-commit install` before contributing

### Assumptions

I did not add any endpoints to manage creating Patients, Clinicians or Medication
When creating a MedicationRequest, I allowed the payload to specify the attributes for
these related fields, and performed a get_or_create

There's no validation when setting a state for a MedicationRequest, but I assume in the
real world you can't go from cancelled to active or completed to active

No pagination was added to the get endpoint but in a real application these results
would need to have pagination

Built and ran this on Linux, I used the psycopg2-binary package to hopefully work
cross-platform but was unable to test
