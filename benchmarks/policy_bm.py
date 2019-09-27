"""
    Policy tests
"""

import pytest

from policy.conditions.logic import Or
from policy.conditions import CIDR
from policy.conditions import Gt
from policy.conditions import Equals
from pyabac.inquiry import Inquiry
from pyabac.policy import Policy


class TestPolicy(object):

    @pytest.mark.parametrize("policy, inquiry, result", [
        (Policy(subjects=[{"name": Equals("admin")}]),
         Inquiry(subject={"name": "admin"}),
         False),
        (Policy(subjects=[{"name": Equals("admin")}]),
         Inquiry(subject={"name": "admin"},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         False),
        (Policy(subjects=[{"name": Equals("admin")}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Equals("GET")}]),
         Inquiry(subject={"name": "admin"},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         True),
        (Policy(subjects=[{"name": Equals("john")}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Equals("GET")}]),
         Inquiry(subject={"name": "admin"},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         False),
        (Policy(subjects=[{"name": Equals("admin"), "age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Equals("GET")}]),
         Inquiry(subject={"name": "admin"},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         False),
        (Policy(subjects=[{"name": Equals("admin"), "age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Equals("GET")}]),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         False),
        (Policy(subjects=[{"name": Equals("admin"), "age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Equals("GET")}]),
         Inquiry(subject={"name": "admin", "age": 40},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         True),
        (Policy(subjects=[{"name": Equals("admin")}, {"age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Equals("GET")}]),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         True),
        (Policy(subjects=[{"name": Equals("admin")}, {"age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Equals("GET")}]),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"}),
         False),
        (Policy(subjects=[{"name": Equals("admin")}, {"age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Or(Equals("GET"), Equals("PUT"))}]),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"}),
         True),
        (Policy(subjects=[{"name": Equals("admin")}, {"age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Or(Equals("GET"), Equals("PUT"))}],
                context={"ip": CIDR("127.0.0.0/24")}),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"}),
         False),
        (Policy(subjects=[{"name": Equals("admin")}, {"age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Or(Equals("GET"), Equals("PUT"))}],
                context={"ip": CIDR("127.0.0.0/24")}),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"},
                 context={"ip": "192.168.1.100"}),
         False),
        (Policy(subjects=[{"name": Equals("admin")}, {"age": Gt(30)}],
                resources=[{"url": Equals("/api/v1/health")}],
                actions=[{"method": Or(Equals("GET"), Equals("PUT"))}],
                context={"ip": CIDR("127.0.0.0/24")}),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"},
                 context={"ip": "127.0.0.10"}),
         True),
    ])
    def test_fits(self, policy, inquiry, result, benchmark):
        fits = benchmark(policy.fits, inquiry)
        assert fits == result


if __name__ == '__main__':
    pytest.main()
