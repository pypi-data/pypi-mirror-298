# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import date

from django.db import models
from rest_framework.exceptions import ValidationError


class BusinessEntities(models.Model):
    business_entity_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "business_entities"


class ChangeOrderFiles(models.Model):
    change_order = models.ForeignKey("ChangeOrders", models.DO_NOTHING)
    file = models.ForeignKey("FileUrls", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "change_order_files"


class ChangeOrderMilestones(models.Model):
    change_order = models.ForeignKey("ChangeOrders", models.DO_NOTHING)
    milestone = models.ForeignKey("Milestones", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "change_order_milestones"


class ChangeOrderResourceRates(models.Model):
    month = models.CharField(max_length=40)
    hours = models.DecimalField(max_digits=19, decimal_places=0)
    change_order_resource = models.ForeignKey("ChangeOrderResources", models.CASCADE, related_name="change_order_resource_rates")
    change_order_resource_rate_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = "change_order_resource_rates"


class ChangeOrderResources(models.Model):
    change_order = models.ForeignKey("ChangeOrders", models.DO_NOTHING, related_name="change_order_resources")
    role = models.ForeignKey("Roles", models.DO_NOTHING)
    level = models.ForeignKey("Levels", models.DO_NOTHING)
    currency = models.ForeignKey("Currencies", models.DO_NOTHING)
    region = models.ForeignKey("Regions", models.DO_NOTHING)
    headcount = models.IntegerField()
    change_order_resource_id = models.AutoField(primary_key=True)
    off_card_rate = models.DecimalField(max_digits=19, decimal_places=0, blank=True, null=True)
    rate_card_rate = models.DecimalField(max_digits=19, decimal_places=0, blank=True, null=True)
    monthly_hours = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "change_order_resources"


class ChangeOrders(models.Model):
    SAVED = 1
    SUBMITTED = 2

    STATUS_CHOICES = [
        (SAVED, "Saved"),
        (SUBMITTED, "Submitted"),
    ]

    change_order_id = models.AutoField(primary_key=True)
    work_order = models.ForeignKey("WorkOrders", models.DO_NOTHING, related_name="change_orders")
    end_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    final_contract_file = models.TextField(blank=True, null=True)
    generated_contract_file = models.TextField(blank=True, null=True)
    infosys_entity = models.ForeignKey("InfosysBusinessEntities", models.DO_NOTHING, null=True)
    change_order_name = models.CharField(max_length=255)
    pricing_model = models.ForeignKey("PricingModels", models.DO_NOTHING, null=True)
    service_type = models.ForeignKey("ServiceTypes", models.DO_NOTHING, null=True)
    milestone_type = models.ForeignKey("MilestoneTypes", models.DO_NOTHING, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=SAVED)
    document_number = models.CharField(max_length=255, blank=True, null=True)
    contract_details = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(blank=True, null=True)
    deleted_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_at = models.DateField(blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    milestones = models.ManyToManyField("Milestones", through="ChangeOrderMilestones")
    files = models.ManyToManyField("FileUrls", through="ChangeOrderFiles")

    class Meta:
        managed = True
        db_table = "change_orders"

    class State(models.TextChoices):
        SAVED = "Saved", "Saved"
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    @property
    def state(self):
        if self.status == self.SAVED:
            return self.State.SAVED
        elif self.end_date is not None:
            if self.end_date > date.today():
                return self.State.ACTIVE
            else:
                return self.State.INACTIVE

    def delete(self, *args, **kwargs):
        if self.status != self.SAVED:
            raise ValidationError(
                f"Cannot delete a change order with status {self.state}. "
                f"Only Saved change orders can be deleted."
            )

        self.is_deleted = True
        self.deleted_by = "User name"  # replace name when we will have authorization
        self.deleted_at = date.today()
        self.save()


class ContractTemplates(models.Model):
    contract_template_id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=255)
    template_content = models.TextField()
    customer = models.ForeignKey("Customers", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "contract_templates"


class Currencies(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "currencies"


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "customers"


class DocumentTypes(models.Model):
    document_type_id = models.AutoField(primary_key=True)
    document_type_name = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "document_types"


class FileUrls(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_url = models.CharField(max_length=5000)
    file_name = models.CharField(max_length=255)
    reference_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "file_urls"


class InfosysBusinessEntities(models.Model):
    infosys_entity_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "infosys_business_entities"


class Levels(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "levels"


class MasterAgreements(models.Model):
    SAVED = 1
    SUBMITTED = 2

    AGREEMENT_STATUS_CHOICES = [
        (SAVED, "Saved"),
        (SUBMITTED, "Submitted"),
    ]

    master_agreement_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    agreement_name = models.CharField(max_length=255)
    agreement_status = models.IntegerField(choices=AGREEMENT_STATUS_CHOICES, default=SAVED)
    created_on = models.DateField()
    expires_on = models.DateField()
    rate_card = models.ForeignKey("RateCards", models.DO_NOTHING)
    agreement_url = models.CharField(max_length=500)
    initial_contract_text = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(blank=True, null=True)
    deleted_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_at = models.DateField(blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "master_agreements"

    class State(models.TextChoices):
        SAVED = "Saved", "Saved"
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    @property
    def state(self):
        if self.agreement_status == self.SAVED:
            return self.State.SAVED
        elif self.expires_on is not None:
            if self.expires_on > date.today():
                return self.State.ACTIVE
            else:
                return self.State.INACTIVE


class MilestoneTypes(models.Model):
    milestone_type_id = models.AutoField(primary_key=True)
    milestone_type_name = models.CharField(max_length=255, blank=True, null=True)
    requires_milestone = models.BooleanField()

    class Meta:
        managed = True
        db_table = "milestone_types"


class Milestones(models.Model):
    milestone_id = models.AutoField(primary_key=True)
    milestone_number = models.IntegerField()
    milestone_description = models.CharField(max_length=255)
    due_date = models.DateField()
    status = models.IntegerField()

    class Meta:
        managed = True
        db_table = "milestones"


class PricingModels(models.Model):
    pricing_model_id = models.AutoField(primary_key=True)
    pricing_model_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "pricing_models"


class RateCardRates(models.Model):
    rate_id = models.AutoField(primary_key=True)
    role = models.ForeignKey("Roles", models.DO_NOTHING)
    level = models.ForeignKey(Levels, models.DO_NOTHING)
    currency = models.ForeignKey(Currencies, models.DO_NOTHING)
    region = models.ForeignKey("Regions", models.DO_NOTHING)
    rate = models.DecimalField(max_digits=19, decimal_places=0)
    rate_card = models.ForeignKey("RateCards", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "rate_card_rates"


class RateCards(models.Model):
    SAVED = 1
    SUBMITTED = 2

    STATUS_CHOICES = [
        (SAVED, "Saved"),
        (SUBMITTED, "Submitted"),
    ]

    rate_card_id = models.AutoField(primary_key=True)
    rate_card_name = models.CharField(max_length=255)
    created_on = models.DateField()
    expires_on = models.DateField()
    status = models.IntegerField(choices=STATUS_CHOICES)

    class Meta:
        managed = True
        db_table = "rate_cards"

    class State(models.TextChoices):
        SAVED = "Saved", "Saved"
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    @property
    def state(self):
        if self.status == self.SAVED:
            return self.State.SAVED
        elif self.expires_on is not None:
            if self.expires_on > date.today():
                return self.State.ACTIVE
            else:
                return self.State.INACTIVE


class Regions(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "regions"


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "roles"


class ServiceDomains(models.Model):
    service_domain_id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "service_domains"


class ServiceRegions(models.Model):
    service_region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "service_regions"


class ServiceTypes(models.Model):
    service_type_id = models.AutoField(primary_key=True)
    service_type_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "service_types"


class WorkOrderFiles(models.Model):
    work_order = models.ForeignKey("WorkOrders", models.DO_NOTHING)
    file = models.ForeignKey(FileUrls, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "work_order_files"


class WorkOrderMilestones(models.Model):
    work_order = models.ForeignKey("WorkOrders", models.DO_NOTHING)
    milestone = models.ForeignKey(Milestones, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "work_order_milestones"


class WorkOrderResourceRates(models.Model):
    month = models.CharField(max_length=40)
    hours = models.DecimalField(max_digits=19, decimal_places=0)
    work_order_resource = models.ForeignKey("WorkOrderResources", models.CASCADE, related_name="work_order_resource_rates")
    work_order_resource_rate_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = "work_order_resource_rates"


class WorkOrderResources(models.Model):
    work_order = models.ForeignKey("WorkOrders", models.DO_NOTHING, related_name="work_order_resources")
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    level = models.ForeignKey(Levels, models.DO_NOTHING)
    currency = models.ForeignKey(Currencies, models.DO_NOTHING)
    region = models.ForeignKey(Regions, models.DO_NOTHING)
    headcount = models.IntegerField()
    work_order_resource_id = models.AutoField(primary_key=True)
    off_card_rate = models.DecimalField(max_digits=19, decimal_places=0, blank=True, null=True)
    rate_card_rate = models.DecimalField(max_digits=19, decimal_places=0, blank=True, null=True)
    monthly_hours = models.IntegerField()

    class Meta:
        managed = True
        db_table = "work_order_resources"


class WorkOrders(models.Model):
    SAVED = 1
    SUBMITTED = 2

    STATUS_CHOICES = [
        (SAVED, "Saved"),
        (SUBMITTED, "Submitted"),
    ]

    work_order_id = models.AutoField(primary_key=True)
    master_agreement = models.ForeignKey(MasterAgreements, models.DO_NOTHING, related_name="work_orders")
    procurement_contract_name = models.CharField(max_length=255, blank=True, null=True)
    procurement_contract_email = models.CharField(max_length=255, blank=True, null=True)
    work_order_name = models.CharField(max_length=255)
    work_order_status = models.IntegerField(choices=STATUS_CHOICES, default=SAVED)
    program_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    work_order_goals = models.TextField(blank=True, null=True)
    infosys_entity = models.ForeignKey(InfosysBusinessEntities, models.DO_NOTHING)
    client_entity = models.ForeignKey(BusinessEntities, models.DO_NOTHING)
    service_domain = models.ForeignKey(ServiceDomains, models.DO_NOTHING)
    service_region = models.ForeignKey(ServiceRegions, models.DO_NOTHING)
    service_type = models.ForeignKey(ServiceTypes, models.DO_NOTHING, null=True)
    pricing_model = models.ForeignKey(PricingModels, models.DO_NOTHING, null=True)
    milestone_type = models.ForeignKey(MilestoneTypes, models.DO_NOTHING, null=True)
    generated_contract_file = models.TextField(blank=True, null=True)
    final_contract_file = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(blank=True, null=True)
    deleted_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_at = models.DateField(blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    contract_details = models.TextField(blank=True, null=True)   # ??? What it is ?
    milestones = models.ManyToManyField(Milestones, through="WorkOrderMilestones")
    files = models.ManyToManyField(FileUrls, through="WorkOrderFiles")
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = "work_orders"

    class State(models.TextChoices):
        SAVED = "Saved", "Saved"
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    @property
    def state(self):
        if self.work_order_status == self.SAVED:
            return self.State.SAVED
        elif self.end_date is not None:
            if self.end_date > date.today():
                return self.State.ACTIVE
            else:
                return self.State.INACTIVE

    def delete(self, *args, **kwargs):
        if self.work_order_status != self.SAVED:
            raise ValidationError(
                f"Cannot delete a work order with status {self.state}. "
                f"Only Saved work orders can be deleted."
            )

        self.is_deleted = True
        self.deleted_by = "User name"  # replace name when we will have authorization
        self.deleted_at = date.today()
        self.save()

class OtherRateCardRates(models.Model):
    rate = models.DecimalField(max_digits=19, decimal_places=0)
    currency = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    rate_card = models.ForeignKey("RateCards", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "other_rate_card_rates"
