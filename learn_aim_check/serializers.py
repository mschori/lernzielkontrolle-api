from rest_framework import serializers

from learn_aim_check.models import ActionCompetence, CheckLearnAim, LearnAim, Tag
from services.group_service import is_user_coach
from users.models import User
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """
    Serializes the Tag model.
    Returns all fields such as tag_name, created_at, updated_at
    """

    class Meta:
        model = Tag
        exclude = ['created_at', 'updated_at']


class LearnAimSerializer(serializers.ModelSerializer):
    """
    Serializes the LearnAim model. Returns all fields such as action_competence, identification, description,
    taxonomy_level, example_text, created_at, updated_at, tags
    """

    tags = TagSerializer(many=True)
    name = serializers.CharField(source='__str__', read_only=True)
    checked = serializers.SerializerMethodField()
    marked_as_todo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LearnAim
        exclude = ['created_at', 'updated_at', 'identification', 'action_competence']

    def get_checked(self, instance):
        """
        Returns all completed learn aims for the current learn aim.
        A completed learn aim is a learn aim that has been closed by a trainee.
        Can be empty because no learn aim has been closed yet.
        :param self: LearnAim object from the database
        :param instance: LearnAim object from the database
        :return: List of all completed learn aims for the current learn aim
        """
        assigned_trainee = self.context['request'].user
        if is_user_coach(self.context['request'].user) and 'student_id' in self.context and User.objects.filter(
                id=self.context['student_id']).exists():
            assigned_trainee = User.objects.get(id=self.context['student_id'])
        completed_learn_aim = CheckLearnAim.objects.filter(closed_learn_check=instance,
                                                           assigned_trainee=assigned_trainee).order_by(
            'close_stage')

        return CheckLearnAimSerializer(completed_learn_aim, many=True, context=self.context).data

    def get_marked_as_todo(self, instance):
        """
        :param instance: LearnAim object from the database
        :return: True if the learn aim is marked as todo
        """
        if 'student_id' in self.context:
            return instance.marked_as_todo.filter(id=self.context['student_id']).exists()
        return False


class SimpleLearnAimSerializer(serializers.ModelSerializer):
    """
    Simplified version of the LearnAimSerializer to avoid recursion.
    """

    tags = TagSerializer(many=True)
    name = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = LearnAim
        exclude = ['created_at', 'updated_at', 'identification', 'action_competence']


class CheckLearnAimSerializer(serializers.ModelSerializer):
    """
    Serializes the CheckLearnAim model.
    Returns all fields such as assigned_trainee, closed_learn_check, comment
    """

    approved_by = UserSerializer(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)
    comment = serializers.CharField(max_length=254, required=True)
    semester = serializers.IntegerField(min_value=1, max_value=8, required=True)
    close_stage = serializers.IntegerField(min_value=1, max_value=3, required=True)
    closed_learn_check_id = serializers.PrimaryKeyRelatedField(queryset=LearnAim.objects.all(),
                                                               source='closed_learn_check', write_only=True)
    learn_aim = SimpleLearnAimSerializer(read_only=True, source='closed_learn_check')

    class Meta:
        model = CheckLearnAim
        fields = '__all__'
        extra_kwargs = {
            'assigned_trainee': {'required': False},
            'closed_learn_check': {'required': False}
        }


class ActionCompetenceSerializer(serializers.ModelSerializer):
    """
    Serializes the ActionCompetence model. Returns all fields such as identification, title, education_ordinance,
    description, associated_modules_vocational_school, associated_modules_overboard_course, created_at, updated_at
    """

    title = serializers.CharField(source='__str__', read_only=True)
    learn_aim = serializers.SerializerMethodField()

    class Meta:
        model = ActionCompetence
        exclude = ['education_ordinance', 'created_at', 'updated_at']

    def get_learn_aim(self, instance):
        """
        :param self: ActionCompetence object from the database
        :param instance: ActionCompetence object from the database
        :return: List of all learn aims for the current action competence
        """
        learn_aims = LearnAim.objects.filter(action_competence=instance).order_by('identification')
        return LearnAimSerializer(learn_aims, many=True, context=self.context).data


class DiagramSerializer(serializers.Serializer):
    """
    Serializer for the chart.
    Returns all fields such as id, name, closed, total
    """
    id = serializers.IntegerField(source='pk')
    name = serializers.CharField(source='__str__')
    closed = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = ActionCompetence
        exclude = ['education_ordinance', 'created_at', 'updated_at']

    def get_total(self, instance) -> int:
        """
        :param self: ActionCompetence object from the database
        :param instance: ActionCompetence object from the database
        :return: Total amount of learn aims for the current action competence
        """
        return LearnAim.objects.filter(action_competence=instance).count()

    def get_closed(self, instance) -> int:
        """
        :param self: ActionCompetence object from the database
        :param instance: ActionCompetence object from the database
        :return: Total amount of approved learn aims for the current action competence
        """
        return CheckLearnAim.objects.filter(closed_learn_check__action_competence=instance,
                                            assigned_trainee=self.context['request'].user, close_stage=3,
                                            is_approved=True).count()


class ToggleTodoSerializer(serializers.ModelSerializer):
    """
    Serializer for toggling the marked_as_todo field of a LearnAim instance.

    This serializer handles updating the marked_as_todo field of a LearnAim instance,
    allowing it to be marked or unmarked as a to-do item.

    :param marked_as_todo: Boolean indicating if the learn aim is marked as a to-do item.
    """

    class Meta:
        model = LearnAim
        fields = ['marked_as_todo']

    def update(self, instance, validated_data):
        instance.marked_as_todo = validated_data.get('marked_as_todo', instance.marked_as_todo)
        instance.save()
        return instance


class UserLearnDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, including related learn aims and tags.

    :param learn_aims: A list of learn aims associated with the user.
    :param tags: A list of tags associated with the user, serialized using the TagSerializer.
    """
    learn_aims = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'firstname', 'lastname', 'learn_aims', 'tags']

    def get_learn_aims(self, obj):
        learn_aims = LearnAim.objects.filter(
            checklearnaim__assigned_trainee=obj
        ).distinct()
        return LearnAimSerializer(learn_aims, many=True, context={'request': self.context['request']}).data
