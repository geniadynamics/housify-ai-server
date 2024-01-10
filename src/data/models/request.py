from tortoise import fields
from tortoise.models import Model


class Image(Model):
    """ """

    hash = fields.BinaryField(pk=True)
    user_id = fields.UUIDField()

    res_x_AIgenerated = fields.IntField()
    res_y_AIgenerated = fields.IntField()
    raw_metadata_AIgenerated = fields.TextField(null=True)
    file_name_AIgenerated = fields.CharField(max_length=256)
    classification_AIgenerated = fields.CharField(max_length=64)

    res_x_AI_original = fields.IntField()
    res_y_AI_original = fields.IntField()
    raw_metadata_original = fields.TextField()
    file_name_original = fields.CharField(max_length=256)
    classification_original = fields.CharField(max_length=64)

    is_watermarked = fields.BooleanField(default=True)
    rating = fields.FloatField(default=-1.0)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class InferenceModel(Model):
    """ """

    name = fields.TextField()
    i_type = fields.TextField()
    hash = fields.BinaryField(null=True)  #!TODO change
    active = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class ImgEdit(Model):
    """ """

    id = fields.UUIDField(pk=True)

    request_id = fields.UUIDField()
    image_id = fields.UUIDField()
    model_id = fields.UUIDField()

    prompt = fields.TextField()


class ImgGeneration(Model):
    """ """

    id = fields.UUIDField(pk=True)

    request_id = fields.UUIDField()
    image_id = fields.UUIDField()
    model_id = fields.UUIDField()

    prompt = fields.TextField()


class Usage(Model):
    """ """

    user_id = fields.UUIDField(pk=True)

    request_type = fields.CharField(max_length=128)
    gpu_time_used = fields.IntField()

    last_request_time = fields.DatetimeField(auto_now=True)


class ImgClassification(Model):
    """ """

    id = fields.UUIDField(pk=True)

    model_id = fields.UUIDField()
    value = fields.CharField(max_length=64)

    processed_at = fields.DatetimeField(auto_now_add=True)


class ImgGenAiDescription(Model):
    """ """

    id = fields.UUIDField(pk=True)

    model_id = fields.UUIDField()
    value = fields.CharField(max_length=64)

    processed_at = fields.DatetimeField(auto_now_add=True)


class Request(Model):
    id = fields.UUIDField(pk=True)
    user = fields.CharField(max_length=256, null=True)

    input = fields.TextField()

    img_input = fields.CharField(max_length=256, null=True)
    img_output = fields.CharField(max_length=256, null=True)

    output_description = fields.TextField(null=True)
    output_classification = fields.CharField(max_length=128, null=True)

    request_classification = fields.FloatField()
    is_public = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    finished_at = fields.DatetimeField(auto_now=True)
    finished_state = fields.CharField(default="computed", max_length=128)


# class Request(Model):
#     """ """
#
#     id = fields.UUIDField(pk=True)
#     is_public = fields.BooleanField(default=False)
#
#     user_id = fields.UUIDField()
#     request_type = fields.CharField(max_length=128)
#
#     created_at = fields.DatetimeField(auto_now_add=True)
#     finished_at = fields.DatetimeField(auto_now=True)
#
#     usage = fields.OneToOneField("usage", related_name="Request")
#
#     image_edits = fields.ReverseRelation[ImgEdit]
#     image_generation = fields.ReverseRelation[ImgGeneration]
