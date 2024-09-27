import unittest
from config import Config

class TestConfigMethods(unittest.TestCase):

    config = Config("configs/test_config2.json")
    def test_config_loading(self):
        self.config.load_json_config()
        self.assertNotEqual(self.config.config, None)

    def test_config_example_reading_source_params(self):
        self.config.load_json_config()
        self.assertEqual(self.config.config["source"]["host"], "https://bdu.fstec.ru/")
        self.assertEqual(self.config.config["source"]["port"], 443)
        self.assertEqual(self.config.config["source"]["type"], 2)
        self.assertEqual(self.config.config["source"]["files_dir"], "BDU_FSTEK")

    def test_config_example_reading_evasion_params(self):
        self.config.load_json_config()
        self.assertEqual(self.config.config["evasion"]["proxy"], 1)
        self.assertEqual(self.config.config["evasion"]["vpn"], 0)
        self.assertEqual(self.config.config["evasion"]["robots"], 0)
        self.assertEqual(self.config.config["evasion"]["sleep"], 1)
        self.assertEqual(self.config.config["evasion"]["captcha"], 0)


if __name__ == '__main__':
    unittest.main()

