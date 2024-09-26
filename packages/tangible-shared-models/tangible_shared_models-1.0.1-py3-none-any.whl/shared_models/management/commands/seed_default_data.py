import os
import json
import sys
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from shared_models.models import (
    Regions, Levels, Currencies, Roles, RateCardRates, RateCards, MasterAgreements,
    Customers, ServiceDomains, BusinessEntities, InfosysBusinessEntities, ServiceRegions,
    MilestoneTypes, PricingModels, ServiceTypes
)

current_directory = os.path.dirname(__file__)


class Command(BaseCommand):
    help = "Seed the database with data from JSON files"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        def load_json_file(file_name):
            file_path = os.path.join(current_directory, file_name)
            try:
                with open(file_path, "r", errors="replace") as file:
                    return json.load(file)
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f"File {file_name} not found. Please check the file path."))
                sys.exit(1)
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR(f"File {file_name} is not a valid JSON file."))
                sys.exit(1)

        try:
            # Seed Customer
            self.stdout.write(self.style.WARNING('Creating Customer...'))
            customer, _ = Customers.objects.get_or_create(customer_name="Nike")

            # Seed RateCard
            self.stdout.write(self.style.WARNING('Creating RateCard...'))
            rate_card, _ = RateCards.objects.get_or_create(
                rate_card_name="Rate Card",
                created_on=datetime.strptime("01/01/2024", "%m/%d/%Y"),
                expires_on=datetime.strptime("05/31/2025", "%m/%d/%Y"),
                status=RateCards.SAVED
            )

            # Seed MasterAgreement
            self.stdout.write(self.style.WARNING('Creating MasterAgreement...'))
            MasterAgreements.objects.get_or_create(
                agreement_name="Master Application Development and Maintenance Agreement",
                customer=customer,
                created_on=datetime.strptime("01/01/2024", "%m/%d/%Y"),
                expires_on=datetime.strptime("05/31/2025", "%m/%d/%Y"),
                rate_card=rate_card,
            )

            # Seed RateCardRates
            self.stdout.write(self.style.WARNING('Creating RateCardRates...'))
            rate_card_rates_data = load_json_file("rate_card_rates.json")
            if rate_card_rates_data:
                rate_card_rates = [
                    RateCardRates(
                        region=Regions.objects.get_or_create(region_name=entry["region_id"])[0],
                        level=Levels.objects.get_or_create(level_name=entry["level_id"])[0],
                        currency=Currencies.objects.get_or_create(currency_name=entry["currency_id"])[0],
                        role=Roles.objects.get_or_create(role_name=entry["role_id"])[0],
                        rate=entry["rate"],
                        rate_card=rate_card
                    )
                    for entry in rate_card_rates_data
                ]
                RateCardRates.objects.bulk_create(rate_card_rates)

            # Seed ServiceDomains
            self.stdout.write(self.style.WARNING('Creating ServiceDomains...'))
            service_domains_data = load_json_file("service_domains.json")
            if service_domains_data:
                service_domains = [
                    ServiceDomains(domain_name=entry["domain_name"])
                    for entry in service_domains_data
                ]
                ServiceDomains.objects.bulk_create(service_domains)

            # Seed BusinessEntities
            self.stdout.write(self.style.WARNING('Creating BusinessEntities...'))
            business_entities_data = load_json_file("business_entities.json")
            if business_entities_data:
                business_entities = [
                    BusinessEntities(entity_name=entry["entity_name"])
                    for entry in business_entities_data
                ]
                BusinessEntities.objects.bulk_create(business_entities)

            # Seed InfosysBusinessEntities
            self.stdout.write(self.style.WARNING('Creating InfosysBusinessEntities...'))
            infosys_business_entities_data = load_json_file("infosys_business_entities.json")
            if infosys_business_entities_data:
                infosys_business_entities = [
                    InfosysBusinessEntities(entity_name=entry["entity_name"])
                    for entry in infosys_business_entities_data
                ]
                InfosysBusinessEntities.objects.bulk_create(infosys_business_entities)

            # Seed ServiceRegions
            self.stdout.write(self.style.WARNING('Creating ServiceRegions...'))
            service_regions_data = load_json_file("service_regions.json")
            if service_regions_data:
                service_regions = [
                    ServiceRegions(region_name=entry["region_name"])
                    for entry in service_regions_data
                ]
                ServiceRegions.objects.bulk_create(service_regions)

            # Seed MilestoneTypes
            self.stdout.write(self.style.WARNING('Creating MilestoneTypes...'))
            milestone_types_data = load_json_file("milestone_types.json")
            if milestone_types_data:
                milestone_types = [
                    MilestoneTypes(
                        milestone_type_name=entry["milestone_type_name"],
                        requires_milestone=entry["requires_milestone"]
                    )
                    for entry in milestone_types_data
                ]
                MilestoneTypes.objects.bulk_create(milestone_types)

            # Seed PricingModels
            self.stdout.write(self.style.WARNING('Creating PricingModels...'))
            pricing_models_data = load_json_file("pricing_models.json")
            if pricing_models_data:
                pricing_models = [
                    PricingModels(pricing_model_name=entry["pricing_model_name"])
                    for entry in pricing_models_data
                ]
                PricingModels.objects.bulk_create(pricing_models)

            # Seed ServiceTypes
            self.stdout.write(self.style.WARNING('Creating ServiceTypes...'))
            service_types_data = load_json_file("service_types.json")
            if service_types_data:
                service_types = [
                    ServiceTypes(service_type_name=entry["service_type_name"])
                    for entry in service_types_data
                ]
                ServiceTypes.objects.bulk_create(service_types)

            self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Seeding failed: {str(e)}"))
            sys.exit(1)

