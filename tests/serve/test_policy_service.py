import json

from blaze.action import ActionSpace, Policy
from blaze.config.client import get_random_client_environment
from blaze.environment import Environment
from blaze.model.model import ModelInstance, SavedModel
from blaze.proto import policy_service_pb2
from blaze.serve.policy_service import PolicyService

from tests.mocks.agent import MockAgent, mock_agent_with_action_space
from tests.mocks.config import get_push_groups, convert_push_groups_to_push_pairs
from tests.mocks.serve import get_page, MockGRPCServicerContext


class TestPolicyService:
    def setup(self):
        self.client_environment = get_random_client_environment()
        self.page = get_page("http://example.com", self.client_environment)
        self.push_groups = get_push_groups()
        self.trainable_push_groups = [group for group in self.push_groups if group.trainable]
        self.action_space = ActionSpace(self.trainable_push_groups)
        self.saved_model = SavedModel(mock_agent_with_action_space(self.action_space), Environment, "", {})

    def test_init(self):
        ps = PolicyService(self.saved_model)
        assert ps
        assert isinstance(ps, PolicyService)
        assert ps.saved_model is self.saved_model
        assert not ps.policies

    def test_get_policy(self):
        ps = PolicyService(self.saved_model)
        policy = ps.GetPolicy(self.page, MockGRPCServicerContext())
        assert policy
        assert isinstance(policy, policy_service_pb2.Policy)
        # Temporarily disable caching policies
        # assert len(ps.policies) == 1
        # assert ps.policies[self.page.url] is policy

    def test_get_policy_returns_cached(self):
        ps = PolicyService(self.saved_model)
        first_policy = ps.GetPolicy(self.page, MockGRPCServicerContext())
        second_policy = ps.GetPolicy(self.page, MockGRPCServicerContext())
        # assert first_policy is second_policy
        # Temporarily disable caching policies
        # assert len(ps.policies) == 1
        # assert ps.policies[self.page.url] is first_policy

    def test_create_push_policy(self):
        ps = PolicyService(self.saved_model)
        policy = ps.create_policy(self.page)
        assert policy
        assert isinstance(policy, policy_service_pb2.Policy)
        push_pairs = convert_push_groups_to_push_pairs(self.push_groups)
        push_pairs = [(s.url, p.url) for (s, p) in push_pairs]
        p = Policy.from_dict(json.loads(policy.policy))
        for (source, push_res) in p.push:
            for push in push_res:
                assert (source.url, push.url) in push_pairs

    def test_create_model_instance(self):
        ps = PolicyService(self.saved_model)
        model_instance = ps.create_model_instance(self.page)
        assert isinstance(model_instance, ModelInstance)
        assert isinstance(model_instance.agent, MockAgent)
        assert model_instance.config.client_env.bandwidth == self.client_environment.bandwidth
        assert model_instance.config.client_env.latency == self.client_environment.latency
        assert model_instance.config.env_config.push_groups == self.push_groups
