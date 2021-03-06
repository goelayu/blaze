import os
import pytest
import tempfile
from unittest import mock

from blaze.command.train import train
from blaze.config.config import get_config
from blaze.config.train import TrainConfig
from tests.mocks.config import get_env_config


class TestTrain:
    def test_train_exits_with_invalid_arguments(self):
        with pytest.raises(SystemExit):
            train([])

    def test_train_invalid_website_file(self):
        with pytest.raises(IOError):
            train(["experiment_name", "--manifest_file", "/non/existent/file"])

    def test_train_with_resume_and_no_resume(self):
        with pytest.raises(SystemExit):
            train(["experiment_name", "--manifest_file", "/tmp/manifest_file", "--resume", "--no-resume"])

    @mock.patch("blaze.model.a3c.train")
    def test_train_a3c(self, mock_train):
        env_config = get_env_config()
        train_config = TrainConfig(experiment_name="experiment_name", num_workers=4)
        config = get_config(env_config, reward_func=1, use_aft=False)
        with tempfile.NamedTemporaryFile() as env_file:
            env_config.save_file(env_file.name)
            train(
                [
                    train_config.experiment_name,
                    "--workers",
                    str(train_config.num_workers),
                    "--model",
                    "A3C",
                    "--manifest_file",
                    env_file.name,
                ]
            )

        mock_train.assert_called_once()
        mock_train.assert_called_with(train_config, config)

    @mock.patch("blaze.model.apex.train")
    def test_train_apex(self, mock_train):
        env_config = get_env_config()
        train_config = TrainConfig(experiment_name="experiment_name", num_workers=4)
        config = get_config(env_config, reward_func=1, use_aft=False)
        with tempfile.NamedTemporaryFile() as env_file:
            env_config.save_file(env_file.name)
            train(
                [
                    train_config.experiment_name,
                    "--workers",
                    str(train_config.num_workers),
                    "--model",
                    "APEX",
                    "--manifest_file",
                    env_file.name,
                ]
            )

        mock_train.assert_called_once()
        mock_train.assert_called_with(train_config, config)

    @mock.patch("blaze.model.ppo.train")
    def test_train_ppo(self, mock_train):
        env_config = get_env_config()
        train_config = TrainConfig(experiment_name="experiment_name", num_workers=4)
        config = get_config(env_config, reward_func=1, use_aft=False)
        with tempfile.NamedTemporaryFile() as env_file:
            env_config.save_file(env_file.name)
            train(
                [
                    train_config.experiment_name,
                    "--workers",
                    str(train_config.num_workers),
                    "--model",
                    "PPO",
                    "--manifest_file",
                    env_file.name,
                ]
            )

        mock_train.assert_called_once()
        mock_train.assert_called_with(train_config, config)

    @mock.patch("blaze.model.apex.train")
    def test_train_resume(self, mock_train):
        env_config = get_env_config()
        train_config = TrainConfig(experiment_name="experiment_name", num_workers=4, resume=True)
        config = get_config(env_config, reward_func=1, use_aft=False)
        with tempfile.NamedTemporaryFile() as env_file:
            env_config.save_file(env_file.name)
            train(
                [
                    train_config.experiment_name,
                    "--workers",
                    str(train_config.num_workers),
                    "--model",
                    "APEX",
                    "--manifest_file",
                    env_file.name,
                    "--resume",
                ]
            )

        mock_train.assert_called_once()
        mock_train.assert_called_with(train_config, config)

    @mock.patch("blaze.model.apex.train")
    def test_train_no_resume(self, mock_train):
        env_config = get_env_config()
        train_config = TrainConfig(experiment_name="experiment_name", num_workers=4, resume=False)
        config = get_config(env_config, reward_func=1, use_aft=False)
        with tempfile.NamedTemporaryFile() as env_file:
            env_config.save_file(env_file.name)
            train(
                [
                    train_config.experiment_name,
                    "--workers",
                    str(train_config.num_workers),
                    "--model",
                    "APEX",
                    "--manifest_file",
                    env_file.name,
                    "--no-resume",
                ]
            )

        mock_train.assert_called_once()
        mock_train.assert_called_with(train_config, config)

    @mock.patch("blaze.model.apex.train")
    def test_train_with_use_aft(self, mock_train):
        env_config = get_env_config()
        train_config = TrainConfig(experiment_name="experiment_name", num_workers=4)
        config = get_config(env_config, reward_func=1, use_aft=True)
        with tempfile.NamedTemporaryFile() as env_file:
            env_config.save_file(env_file.name)
            train(
                [
                    train_config.experiment_name,
                    "--workers",
                    str(train_config.num_workers),
                    "--model",
                    "APEX",
                    "--manifest_file",
                    env_file.name,
                    "--use_aft",
                ]
            )

        mock_train.assert_called_once()
        mock_train.assert_called_with(train_config, config)

    @mock.patch("blaze.model.apex.train")
    def test_train_with_reward_func(self, mock_train):
        env_config = get_env_config()
        train_config = TrainConfig(experiment_name="experiment_name", num_workers=4)
        config = get_config(env_config, reward_func=3, use_aft=False)
        with tempfile.NamedTemporaryFile() as env_file:
            env_config.save_file(env_file.name)
            train(
                [
                    train_config.experiment_name,
                    "--workers",
                    str(train_config.num_workers),
                    "--model",
                    "APEX",
                    "--manifest_file",
                    env_file.name,
                    "--reward_func",
                    "3",
                ]
            )

        mock_train.assert_called_once()
        mock_train.assert_called_with(train_config, config)
