import unittest
import jira_request as jr
import dictionary_funcs as df

class TestJiraFunctions(unittest.TestCase):

    def test_key_filter(self) -> None:
        self.assertEqual(jr.key_filter(["1","2","3"],"1"), True)
        self.assertEqual(jr.key_filter(["1","2","3"],"3"), True)
        self.assertEqual(jr.key_filter(["1","2","3"],"10"), False)

    def test_iter_dict(self) -> None:
        D0 = {}
        L0 = []
        L1 = ["1"]
        L2 = ["1",2,3]
        D1 = {"K1D1":"V1"}
        D2 = {"K1D1":"V1", "K2D1":"V2", "K3D1":"V3"}
        D3 = {"K1D3":"V1","K2D3":"V2","K3D3":"V3"}
        D4 = {"K1D2":"V1","K2D2":"V2","K3D2":D3}
        D5 = {"K1D1":D0}
        D6 = {"K1D1":"V1", "K2D1":"V2", "K3D1":D4}
        D7 = {"K1D1":"V1", "K2D1":"V2", "K3D1":L2}
        D8 = {"K1":None, "K2":None, "K3":None}
        A1 = {"K1D1":"V1","K2D1":"V2","K3D1/K1D2":"V1","K3D1/K2D2":"V2","K3D1/K3D2/K1D3":"V1","K3D1/K3D2/K2D3":"V2","K3D1/K3D2/K3D3":"V3"}
        A2 = {"K1D1":"V1","K2D1":"V2","K3D1/0":"1","K3D1/1":2,"K3D1/2":3}
        self.assertEqual(jr.iter_dict(D0),D0, "Test iter_dict with empty dict failed")
        self.assertEqual(jr.iter_dict(D1),D1, "Test iter_dict with 1 element and depth of 1 failed")
        self.assertEqual(jr.iter_dict(D2),D2, "Test iter_dict with 3 element and depth of 1 failed")
        self.assertEqual(jr.iter_dict(D5),{}, "Test iter_dict with 1 element and depth of 2 failed")
        self.assertEqual(jr.iter_dict(D6),A1, "Test iter_dict with 3 element and depth of 3 failed")
        self.assertEqual(jr.iter_dict(D7),A2, "Test iter_dict with 3 element and depth of 3 failed")
        self.assertEqual(jr.iter_dict(D8),{}, "Test None failed")

    def test_iter_list(self) -> None:
        L0 = []
        L1 = ["1"]
        L2 = ["1",2,3]
        D0 = {}
        D1 = {"K1D1":"V1"}
        D2 = {"K1D1":"V1", "K2D1":"V2", "K3D1":"V3"}
        L3 = [D2,2,3]
        L4 = ["1",2,D2]
        self.assertEqual(jr.iter_list(L0),{}, "Base Case Test - empty array")
        self.assertEqual(jr.iter_list(L1),{"0":"1"}, "Normal Test - 1 element array")
        self.assertEqual(jr.iter_list(L2),{"0":"1","1":2,"2":3}, "Normal Test - 3 element array")
        self.assertEqual(jr.iter_list(L3),{"0/K1D1":"V1","0/K2D1":"V2","0/K3D1":"V3","1":2,"2":3}, "Normal Test - 3 element array depth 2 (pos1)")
        self.assertEqual(jr.iter_list(L4),{"0":"1","1":2,"2/K1D1":"V1","2/K2D1":"V2","2/K3D1":"V3"}, "Normal Test - 3 element array depth 2 (pos3)")

    def test_prepend_key(self) -> None:
        D0 = {}
        D1 = {"0":"1"}
        D2 = {"0":"1","1":2,"2/K1D1":"V1","2/K2D1":"V2","2/K3D1":"V3"}
        self.assertEqual(jr.prepend_key("asdf",D0),{},"base case test - empty dict")
        self.assertEqual(jr.prepend_key("Brian/test/",D1),{"Brian/test/0":"1"},"Normal test - 1 element dict")
        self.assertEqual(jr.prepend_key("Brian/test/",D2),{"Brian/test/0":"1","Brian/test/1":2,"Brian/test/2/K1D1":"V1","Brian/test/2/K2D1":"V2","Brian/test/2/K3D1":"V3"},"Normal test - 4 element dict")

class TestDictionaryFunctions(unittest.TestCase):

    def test_dictionary_compare(self) -> None:
        jira_url = "https://control-associates.atlassian.net"
        project_key = "MBPP"
        username = "bsauerborn@control-associates.com"
        password_or_api_token = "ATATT3xFfGF0rV8vMjTWh3UqKvbXw3uHVfcKleNp8N7O5h6D5k51jI16sEvujZkkl3M5gfmba-fvCrixImyhjsS_ChMZdbyYKmdmAc8A722TdQNr62GiiGgTLMg6AGTARhg_oRp88aRCMwx1TQ-UdS5hq4355R0zDcBC9rSNgSX7uZocbfgTvEA=9EC2BB84"

        # JQL (Jira Query Language) to filter issues by project
        jql = f"project={project_key}"
        
        D0 = {}
        D1 = {"K1":"V1"}
        C1 = {"K3":"V3"}
        D2 = {"K1":"V1","K2":"V2","K3":"V3"}
        D3 = {"K1":1,"K2":2,"K3":3}
        D4 = {"K1":None,"K2":None,"K3":None}
        D5 = jr.iter_dict(jr.get_jira_project_issues(username, password_or_api_token, jql, jr.generate_jira_url(jira_url)))
        self.assertEqual(df.dictionary_compare(D0,D0),{},"base case test 1")
        self.assertEqual(df.dictionary_compare(D0,D1),{},"base case test 2")
        self.assertEqual(df.dictionary_compare(D1,D0),D1,"normal test (1 element empty comp array)")
        self.assertEqual(df.dictionary_compare(D1,D1),{},"normal test (1 element full comp array)")
        self.assertEqual(df.dictionary_compare(D2,C1),{"K1":"V1","K2":"V2"},"normal test (3 element partial comp array)")
        self.assertEqual(df.dictionary_compare(D2,D2),{},"normal test (1 element full comp array)")
        self.assertEqual(df.dictionary_compare(D3,D3),{},"normal test (1 element full comp array)")
        self.assertEqual(df.dictionary_compare(D5,D5),{},"normal test (1 element full comp array)")

if __name__ == '__main__':
    unittest.main()