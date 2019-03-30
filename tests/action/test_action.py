import collections
import copy
import itertools

from blaze.action import Action, ActionSpace

from tests.mocks.config import get_push_groups

class TestAction():
  def setup(self):
    self.push_groups = get_push_groups()

  def test_init(self):
    a = Action(0, 0, 0, 0, self.push_groups)
    assert isinstance(a, Action)

  def test_source(self):
    a = Action(2, 0, 0, 2, self.push_groups)
    assert a.source == self.push_groups[0].resources[0]

    a = Action(3, 1, 0, 1, self.push_groups)
    assert a.source == self.push_groups[1].resources[0]

  def test_push(self):
    a = Action(2, 0, 0, 2, self.push_groups)
    assert a.push == self.push_groups[0].resources[2]

    a = Action(3, 1, 0, 1, self.push_groups)
    assert a.push == self.push_groups[1].resources[1]

  def test_noop(self):
    a = Action(0, 0, 0, 0, self.push_groups)
    assert a.is_noop

  def test_eq(self):
    a1 = Action(action_id=5)
    a2 = Action(action_id=5)
    assert a1 == a2

class TestActionSpace():
  def setup(self):
    self.push_groups = get_push_groups()
    self.action_space = ActionSpace(self.push_groups)
    self.sampled_actions = collections.Counter(self.action_space.sample() for i in range(1000))

  def test_init_push_resources(self):
    # pushable resources are all resources except the first in each group
    assert len(self.action_space.push_resources) == 3
    assert self.action_space.push_resources[0].order == 2
    assert self.action_space.push_resources[1].order == 3
    assert self.action_space.push_resources[2].order == 4

  def test_init_actions(self):
    # 3 for the first group, 1 for the second, and 1 no-op
    assert len(self.action_space.actions) == 5
    # ensure all actions are unique
    assert len(set((action.g, action.s, action.p) for action in self.action_space.actions)) == 5
    # ensure all push urls are after the source urls
    assert all(action.p > action.s for action in self.action_space.actions if not action.is_noop)

  def test_seed(self):
    a = ActionSpace(self.push_groups)
    a.seed(100)

  def test_sample_returns_noop(self):
    assert 0 in self.sampled_actions

  def test_sample_returns_all_actions(self):
    assert len(self.sampled_actions) == len(self.action_space.actions)

  def test_sample_returns_more_earlier_resources(self):
    # map action IDs to actions and their count
    actions = ((self.action_space.decode_action_id(action_id), size)
               for (action_id, size) in self.sampled_actions.items())
    # remove no-ops
    actions = (action for action in actions if not action[0].is_noop)
    # sort them by the order in which the push resources appear
    actions = sorted(actions, key=lambda a: a[0].push.order)
    # group by the push resource
    actions = itertools.groupby(actions, key=lambda a: a[0].push.order)
    # transform from (action_id, [(Action, count), (Action, count), ...])
    #  to (action_id, [count, count, ...])
    actions = itertools.starmap(lambda k, g: (k, map(lambda a: a[1], g)), actions)
    # sum up the counts for each action_id
    actions = itertools.starmap(lambda k, g: (k, sum(g)), actions)
    # get a subscriptable list
    actions = list(actions)
    # for each consecutive pair, ensure that earlier push resources are selected
    #  more often
    for i, j in zip(actions[:-1], actions[1:]):
      assert i[1] > j[1]

  def test_sample_does_not_return_used_push_resource(self):
    action_space = copy.deepcopy(self.action_space)
    limit = len(action_space.push_resources)

    # go through all of the actions, but set a hard limit
    while limit > 0:
      action_id = action_space.sample()
      a = action_space.decode_action_id(action_id)
      if a.is_noop:
        continue
      action_space.use_action(a)
      assert a.push not in action_space.push_resources
      if not action_space:
        break
      limit -= 1
    else:
      assert False, 'Did not cycle through all push resources'