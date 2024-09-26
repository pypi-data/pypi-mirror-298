# Django Python Tangible Shared

This repository contains the `tangible_shared` Django app, which provides shared models and utilities to be used across various Django projects. This app centralizes the models that are common to multiple applications within the Tangible ecosystem.

## Prerequisites

Before running migrations or starting any development work, ensure the following prerequisites are met:

1. **PostgreSQL Database Setup:**
   - A PostgreSQL database named `tangible` must be created manually.
   - A schema within this database also named `tangible` must be created.

   You can create the database and schema using the following SQL commands:

   ```sql
   CREATE DATABASE tangible;
   CREATE SCHEMA tangible;

   ```

   After this is complete please ensure to run the following command to migrate all required data tables and seed data for development:
   ```
   python manage.py migrate
   ```
   
2. **Generate default data:**
   - Generate data for models: Regions, Levels, Currencies, Roles, RateCardRates, RateCards, MasterAgreements, Customers, ServiceDomains, BusinessEntities, InfosysBusinessEntities, ServiceRegions, MilestoneTypes, PricingModels, ServiceTypes
   ```
   python manage.py seed_default_data
   ```
   - Cleanup all DB data
   ```
   python manage.py flush
   ```
