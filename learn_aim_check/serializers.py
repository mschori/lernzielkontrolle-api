from rest_framework import serializers

from learn_aim_check.models import ActionCompetence, CheckLearnAim, LearnAim, Tag
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """
    Serializes the Tag model.
    returns all fields such as tag_name, created_at, updated_at
    """

    class Meta:
        model = Tag
        exclude = ['created_at', 'updated_at']


class CheckLearnAimSerializer(serializers.ModelSerializer):
    """
    Serializes the CheckLearnAim model.
    Returns all fields such as assigned_trainee, closed_learn_check, comment
    """

    approved_by = UserSerializer(read_only=True)
    comment = serializers.CharField(max_length=254, required=True)
    semester = serializers.IntegerField(min_value=1, max_value=8, required=True)
    close_stage = serializers.IntegerField(min_value=1, max_value=3, required=True)
    closed_learn_check_id = serializers.PrimaryKeyRelatedField(queryset=LearnAim.objects.all(),
                                                            source='closed_learn_check', write_only=True)

    class Meta:
        model = CheckLearnAim
        fields = '__all__'
        read_only_fields = ['approved_by']
        extra_kwargs = {
            'assigned_trainee': {'required': False},
            'closed_learn_check': {'required': False}
        }


class LearnAimSerializer(serializers.ModelSerializer):
    """
    Serializes the LearnAim model.
    Returns all fields such as action_competence, identification, description, taxonomy_level, example_text, created_at, updated_at, tags
    """

    tags = TagSerializer(many=True)
    name = serializers.CharField(source='__str__', read_only=True)
    checked = serializers.SerializerMethodField()

    class Meta:
        model = LearnAim
        exclude = ['created_at', 'updated_at', 'identification', 'action_competence']

    def get_checked(self, instance):
        """
        Returns all completed learn aims for the current learn aim.
        A completed learn aim is a learn aim that has been closed by a trainee.
        Can be empty because no learn aim has been closed yet.
        """
        completed_learn_aim = CheckLearnAim.objects.filter(closed_learn_check=instance,
                                                           assigned_trainee=self.context['request'].user)

        return CheckLearnAimSerializer(completed_learn_aim, many=True, context=self.context).data


class ActionCompetenceSerializer(serializers.ModelSerializer):
    """
    Serializes the ActionCompetence model.
    Returns all fields such as identification, title, education_ordinance, description, associated_modules_vocational_school, associated_modules_overboard_course, created_at, updated_at
    """

    title = serializers.CharField(source='__str__', read_only=True)
    learn_aim = serializers.SerializerMethodField()

    class Meta:
        model = ActionCompetence
        exclude = ['education_ordinance', 'created_at', 'updated_at']

    def get_learn_aim(self, instance):
        """
        Returns all learn aims for the current action competence as a list.
        """
        learn_aims = LearnAim.objects.filter(action_competence=instance)
        return LearnAimSerializer(learn_aims, many=True, context=self.context).data
