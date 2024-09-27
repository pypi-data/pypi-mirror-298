# test_PolymorphicMongoListProxy
#
# Since MongoListProxy has been thoroughly exercised elsewhere,
# only test functionality unique to PolymorphicMongoListProxy

from bson import ObjectId
from datetime import datetime
import mongo_objects
from pymongo.collection import Collection
import pytest
import secrets


@pytest.fixture(scope="class")
def getMPMUDClasses(mongo_db):
    """Return a set of polymorphic MongoUserDict classes configured for a per-test-class unique collection"""

    class MyMongoUserDict(mongo_objects.MongoUserDict):
        collection_name = secrets.token_hex(6)
        database = mongo_db

    class MyMongoListProxyA(mongo_objects.PolymorphicMongoListProxy):
        container_name = "proxyA"
        proxy_subclass_map = {}

    class MyMongoListProxyAa(MyMongoListProxyA):
        proxy_subclass_key = "Aa"

    class MyMongoListProxyAb(MyMongoListProxyA):
        proxy_subclass_key = "Ab"

    class MyMongoListProxyAc(MyMongoListProxyA):
        proxy_subclass_key = "Ac"

    class MyMongoListProxyA1(mongo_objects.PolymorphicMongoListProxy):
        container_name = "proxyA1"
        proxy_subclass_map = {}

    class MyMongoListProxyA1a(MyMongoListProxyA1):
        proxy_subclass_key = "A1a"

    class MyMongoListProxyA1b(MyMongoListProxyA1):
        proxy_subclass_key = "A1b"

    class MyMongoListProxyA1c(MyMongoListProxyA1):
        proxy_subclass_key = "A1c"

    class MyMongoListProxyB(mongo_objects.PolymorphicMongoListProxy):
        container_name = "proxyB"
        proxy_subclass_map = {}

    class MyMongoListProxyBa(MyMongoListProxyB):
        proxy_subclass_key = "Ba"

    class MyMongoListProxyBb(MyMongoListProxyB):
        proxy_subclass_key = "Bb"

    class MyMongoListProxyBc(MyMongoListProxyB):
        proxy_subclass_key = "Bc"

    return {
        "parent_doc": MyMongoUserDict,
        "A": MyMongoListProxyA,
        "Aa": MyMongoListProxyAa,
        "Ab": MyMongoListProxyAb,
        "Ac": MyMongoListProxyAc,
        "A1": MyMongoListProxyA1,
        "A1a": MyMongoListProxyA1a,
        "A1b": MyMongoListProxyA1b,
        "A1c": MyMongoListProxyA1c,
        "B": MyMongoListProxyB,
        "Ba": MyMongoListProxyBa,
        "Bb": MyMongoListProxyBb,
        "Bc": MyMongoListProxyBc,
    }


@pytest.fixture(scope="class")
def getPopulatedMPMUDClasses(getMPMUDClasses):

    classes = getMPMUDClasses
    itemMax = 3  # make three of everything

    # make parent objects
    for i in range(itemMax):
        parent = classes["parent_doc"](
            {
                "name": f"Record {i}",
                "amount": i * 10,
            }
        )

        # make "A" proxies include a base-class proxy
        for keyA in ("A", "Aa", "Ab", "Ac"):
            proxyA = classes[keyA].create(
                parent,
                {
                    "nameA": f"Proxy A-{keyA}",
                    "amountA": i * 100,
                },
            )

            # make second-level A1 proxies
            for keyA1 in ("A1", "A1a", "A1b", "A1c"):
                proxyA1 = classes[keyA1].create(
                    proxyA,
                    {
                        "nameA1": f"Proxy A1-{keyA}-{keyA1}",
                        "amountA1": i * 1000,
                    },
                )

        # make "B" proxies
        for keyB in ("B", "Ba", "Bb", "Bc"):
            proxyB = classes[keyB].create(
                parent,
                {
                    "nameB": f"Proxy B-{keyB}",
                    "amountB": i * 100 + 1,
                },
            )

        # save data
        parent.save()

    return classes


@pytest.fixture(scope="class")
def getSampleParent(getPopulatedMPMUDClasses):
    classes = getPopulatedMPMUDClasses
    # find a random entry of the base class
    return classes["parent_doc"].find_one()


@pytest.fixture(scope="class")
def getSampleProxyA(getPopulatedMPMUDClasses, getSampleParent):
    classes = getPopulatedMPMUDClasses
    # return the first proxyA in the list
    return classes["A"].get_proxies(getSampleParent)[0]


@pytest.fixture(scope="class")
def getSampleProxyA1(getPopulatedMPMUDClasses, getSampleProxyA):
    classes = getPopulatedMPMUDClasses
    # return the first proxyA1 in the list
    return classes["A1"].get_proxies(getSampleProxyA)[0]


class TestInitSubclass:
    """Test __init_subclass__ permutations"""

    def test_init_subclass(self):
        class MyTestClassBase(mongo_objects.PolymorphicMongoListProxy):
            # create our own local testing namespace
            proxy_subclass_map = {}

        class MyTestSubclassA(MyTestClassBase):
            proxy_subclass_key = "A"

        class MyTestSubclassB(MyTestClassBase):
            proxy_subclass_key = "B"

        class MyTestSubclassC(MyTestClassBase):
            proxy_subclass_key = "C"

        # Verify that all classes were added to the map
        assert MyTestClassBase.proxy_subclass_map == {
            None: MyTestClassBase,
            "A": MyTestSubclassA,
            "B": MyTestSubclassB,
            "C": MyTestSubclassC,
        }

        # verify our local subclass map namespace didn't affect the module base class map
        assert len(mongo_objects.PolymorphicMongoListProxy.proxy_subclass_map) == 0

    def test_init_subclass_duplicate_key(self):
        with pytest.raises(mongo_objects.MongoObjectsSubclassError):

            class MyTestClassBase(mongo_objects.PolymorphicMongoListProxy):
                # create our own local testing namespace
                proxy_subclass_map = {}

            class MyTestSubclassA(MyTestClassBase):
                proxy_subclass_key = "A"

            class MyTestSubclassAnotherA(MyTestClassBase):
                proxy_subclass_key = "A"


class TestCreate:
    def test_create(self, getPopulatedMPMUDClasses, getSampleProxyA):
        classes = getPopulatedMPMUDClasses
        proxyA = getSampleProxyA
        parent = proxyA.parent

        # record current state
        original = parent.copy()
        count = len(proxyA.get_subdoc_container())

        # create a base class proxy object
        newProxy = classes["A"].create(
            parent, {"name": "new proxyA entry"}, autosave=True
        )

        # Since the base class does not define a proxy_subclass_key, verify none was added to the record
        assert "_psckey" not in newProxy
        assert isinstance(newProxy, classes["A"])

        # verify key was added to the original data
        assert "_sdkey" in newProxy

        # Now create new subclass objects
        for proxy_subclass in ("Aa", "Ab", "Ac"):
            newProxy = classes[proxy_subclass].create(
                parent, {"name": f"new proxy{proxy_subclass} entry"}
            )
            assert newProxy["_psckey"] == proxy_subclass
            assert isinstance(newProxy, classes[proxy_subclass])
            assert "_sdkey" in newProxy

        # verify four new entries created
        assert len(proxyA.get_subdoc_container()) == count + 4
        assert parent["_last_unique_integer"] == original["_last_unique_integer"] + 4

        # confirm the parent document was saved
        assert parent["_updated"] > original["_updated"]

    def test_create_no_save(self, getPopulatedMPMUDClasses, getSampleProxyA):
        classes = getPopulatedMPMUDClasses
        proxyA = getSampleProxyA
        parent = proxyA.parent

        # record current state
        original = parent.copy()
        count = len(proxyA.get_subdoc_container())

        # create a base class proxy object
        newProxy = classes["A"].create(
            parent, {"name": "new proxyA entry"}, autosave=False
        )

        # Since the base class does not define a proxy_subclass_key, verify none was added to the record
        assert "_psckey" not in newProxy
        assert isinstance(newProxy, classes["A"])

        # verify key was added to the original data
        assert "_sdkey" in newProxy

        # Now create new subclass objects
        for proxy_subclass in ("Aa", "Ab", "Ac"):
            newProxy = classes[proxy_subclass].create(
                parent, {"name": f"new proxy{proxy_subclass} entry"}, autosave=False
            )
            assert newProxy["_psckey"] == proxy_subclass
            assert isinstance(newProxy, classes[proxy_subclass])
            assert "_sdkey" in newProxy

        # verify four new entries created
        assert len(proxyA.get_subdoc_container()) == count + 4
        assert parent["_last_unique_integer"] == original["_last_unique_integer"] + 4

        # confirm the parent document was not saved
        assert parent["_updated"] == original["_updated"]

    def test_create_A1(self, getPopulatedMPMUDClasses, getSampleProxyA1):
        classes = getPopulatedMPMUDClasses
        proxyA1 = getSampleProxyA1
        proxyA = proxyA1.parent
        parent = proxyA1.ultimate_parent

        # record current state
        original = parent.copy()
        countA = len(proxyA.get_subdoc_container())
        countA1 = len(proxyA1.get_subdoc_container())

        # create a base class second-level proxy object
        newProxy = classes["A1"].create(
            proxyA, {"name": "new proxyA1 entry"}, autosave=True
        )

        # Since the base class does not define a proxy_subclass_key, verify none was added to the record
        assert "_psckey" not in newProxy
        assert isinstance(newProxy, classes["A1"])

        # Now create new second-level subclass objects
        for key in ("A1a", "A1b", "A1c"):
            newProxy = classes[key].create(proxyA, {"name": f"new proxy{key} entry"})
            assert newProxy["_psckey"] == key
            assert isinstance(newProxy, classes[key])

        # verify four new entries created at the second level
        assert len(proxyA.get_subdoc_container()) == countA
        assert len(proxyA1.get_subdoc_container()) == countA1 + 4
        assert parent["_last_unique_integer"] == original["_last_unique_integer"] + 4

        # confirm the parent document was saved
        assert parent["_updated"] > original["_updated"]

    def test_create_A1_no_save(self, getPopulatedMPMUDClasses, getSampleProxyA1):
        classes = getPopulatedMPMUDClasses
        proxyA1 = getSampleProxyA1
        proxyA = proxyA1.parent
        parent = proxyA1.ultimate_parent

        # record current state
        original = parent.copy()
        countA = len(proxyA.get_subdoc_container())
        countA1 = len(proxyA1.get_subdoc_container())

        # create a base class second-level proxy object
        newProxy = classes["A1"].create(
            proxyA, {"name": "new proxyA1 entry"}, autosave=False
        )

        # Since the base class does not define a proxy_subclass_key, verify none was added to the record
        assert "_psckey" not in newProxy
        assert isinstance(newProxy, classes["A1"])

        # Now create new second-level subclass objects
        for key in ("A1a", "A1b", "A1c"):
            newProxy = classes[key].create(
                proxyA, {"name": f"new proxy{key} entry"}, autosave=False
            )
            assert newProxy["_psckey"] == key
            assert isinstance(newProxy, classes[key])

        # verify four new entries created at the second level
        assert len(proxyA.get_subdoc_container()) == countA
        assert len(proxyA1.get_subdoc_container()) == countA1 + 4
        assert parent["_last_unique_integer"] == original["_last_unique_integer"] + 4

        # confirm the parent document was not saved
        assert parent["_updated"] == original["_updated"]


class TestPolymorphicBasics:
    def test_subclass_map(self, getPopulatedMPMUDClasses):
        """getMPMUDClasses create a new proxy_subclass_map namespace for each proxy base class
        Verify the keys in the proxy_subclass map
        Verify the base class proxy_subclass map is empty"""
        classes = getPopulatedMPMUDClasses
        assert len(mongo_objects.PolymorphicMongoListProxy.proxy_subclass_map) == 0
        assert (
            len(
                set(classes["A"].proxy_subclass_map).difference(
                    [None, "Aa", "Ab", "Ac"]
                )
            )
            == 0
        )
        assert (
            len(
                set(classes["A1"].proxy_subclass_map).difference(
                    [None, "A1a", "A1b", "A1c"]
                )
            )
            == 0
        )
        assert (
            len(
                set(classes["B"].proxy_subclass_map).difference(
                    [None, "Ba", "Bb", "Bc"]
                )
            )
            == 0
        )

    def test_get_proxy(self, getPopulatedMPMUDClasses, getSampleParent):
        """
        Test accessing both first-level and second-level proxies
        """
        classes = getPopulatedMPMUDClasses
        parent = getSampleParent

        # loop through keys in the proxy A container
        for keyA in [entry["_sdkey"] for entry in parent[classes["A"].container_name]]:

            # create a first-level proxy object
            proxyA = classes["A"].get_proxy(parent, keyA)

            # verify dictionary
            assert id(proxyA.data()) == id(
                parent[classes["A"].container_name][proxyA.seq]
            )

            # the base class object won't have _psckey
            if "_psckey" not in proxyA:
                assert isinstance(proxyA, classes["A"])
            else:
                assert isinstance(proxyA, classes[proxyA["_psckey"]])

            # loop through the keys of the second level proxy A1 container
            for keyA1 in [
                entry["_sdkey"]
                for entry in parent[classes["A"].container_name][proxyA.seq][
                    classes["A1"].container_name
                ]
            ]:

                # create a second-level proxy object
                proxyA1 = classes["A1"].get_proxy(proxyA, keyA1)

                # verify dictionary
                assert id(proxyA1.data()) == id(
                    parent[classes["A"].container_name][proxyA.seq][
                        classes["A1"].container_name
                    ][proxyA1.seq]
                )

                # the base class object won't have _psckey
                if "_psckey" not in proxyA1:
                    assert isinstance(proxyA1, classes["A1"])
                else:
                    assert isinstance(proxyA1, classes[proxyA1["_psckey"]])

    def test_get_proxy_by_sequence(self, getPopulatedMPMUDClasses, getSampleParent):
        """
        Test accessing both first-level and second-level proxies
        """
        classes = getPopulatedMPMUDClasses
        parent = getSampleParent

        # loop through keys in the proxy A container
        for seqA in range(len(parent[classes["A"].container_name])):

            # create a first-level proxy object
            proxyA = classes["A"].get_proxy(parent, seq=seqA)

            # verify dictionary
            assert id(proxyA.data()) == id(parent[classes["A"].container_name][seqA])

            # the base class object won't have _psckey
            if "_psckey" not in proxyA:
                assert isinstance(proxyA, classes["A"])
            else:
                assert isinstance(proxyA, classes[proxyA["_psckey"]])

            # loop through the keys of the second level proxy A1 container
            for seqA1 in range(
                len(
                    parent[classes["A"].container_name][proxyA.seq][
                        classes["A1"].container_name
                    ]
                )
            ):

                # create a second-level proxy object
                proxyA1 = classes["A1"].get_proxy(proxyA, seq=seqA1)

                # verify dictionary
                assert id(proxyA1.data()) == id(
                    parent[classes["A"].container_name][seqA][
                        classes["A1"].container_name
                    ][seqA1]
                )

                # the base class object won't have _psckey
                if "_psckey" not in proxyA1:
                    assert isinstance(proxyA1, classes["A1"])
                else:
                    assert isinstance(proxyA1, classes[proxyA1["_psckey"]])

    def test_get_proxy_subclass(self, getPopulatedMPMUDClasses, getSampleParent):
        """
        Test accessing both first-level and second-level proxies with subclasses
        """
        classes = getPopulatedMPMUDClasses
        parent = getSampleParent

        # loop through keys in the proxy A container
        for itemA in parent[classes["A"].container_name]:
            keyA = itemA["_sdkey"]

            # create a first-level proxy object
            # This should always work
            proxyA = classes["A"].get_proxy(parent, keyA)

            # loop through the subclasses
            for subclass in ("Aa", "Ab", "Ac"):
                # we should also be able to locate the proxy with its subclass
                if proxyA.get("_psckey") == subclass:
                    proxyA_by_subclass = classes[subclass].get_proxy(parent, keyA)
                    assert id(proxyA.data()) == id(proxyA_by_subclass.data())

                # creating a proxy with the wrong class raises an exception
                else:
                    with pytest.raises(mongo_objects.MongoObjectsPolymorphicMismatch):
                        proxyA_by_subclass = classes[subclass].get_proxy(parent, keyA)
                        proxyA_by_subclass.keys()

                # loop through the keys of the second level proxy A1 container
                for itemA1 in proxyA[classes["A1"].container_name]:
                    keyA1 = itemA1["_sdkey"]

                    # create a second-level proxy object
                    # This should always work
                    proxyA1 = classes["A1"].get_proxy(proxyA, keyA1)

                    # loop through the subclasses
                    for subclassA1 in ("A1a", "A1b", "A1c"):
                        # we should also be able to locate the proxy with its subclass
                        if proxyA1.get("_psckey") == subclassA1:
                            proxyA1_by_subclass = classes[subclassA1].get_proxy(
                                proxyA, keyA1
                            )
                            assert id(proxyA1.data()) == id(proxyA1_by_subclass.data())

                        # creating a proxy with the wrong class raises an exception
                        else:
                            with pytest.raises(
                                mongo_objects.MongoObjectsPolymorphicMismatch
                            ):
                                proxyA1_by_subclass = classes[subclassA1].get_proxy(
                                    proxyA, keyA1
                                )
                                proxyA1_by_subclass.keys()

    def test_get_proxies(self, getPopulatedMPMUDClasses, getSampleParent):
        """
        Test accessing both first-level and second-level proxies with subclasses
        """
        classes = getPopulatedMPMUDClasses
        parent = getSampleParent

        # collect all first-level proxies from the base class
        proxiesA = list(classes["A"].get_proxies(parent))

        # verify all proxies were found
        assert len(proxiesA) == 4

        # verify proper subclass was returned
        for proxyA in proxiesA:
            assert isinstance(proxyA, classes[proxyA.get("_psckey", "A")])

            # collect all second-level proxies from the base class
            proxiesA1 = list(classes["A1"].get_proxies(proxyA))

            # verify all proxies were found
            assert len(proxiesA1) == 4

            # verify proper subclass was returned
            for proxyA1 in proxiesA1:
                assert isinstance(proxyA1, classes[proxyA1.get("_psckey", "A1")])

    def test_get_proxies_subclass(self, getPopulatedMPMUDClasses, getSampleParent):
        """
        Test accessing both first-level and second-level proxies with subclasses
        """
        classes = getPopulatedMPMUDClasses
        parent = getSampleParent

        # loop through the first-level subclasses
        for subclass in ("Aa", "Ab", "Ac"):
            # collect the proxies from this subclass
            proxiesA = list(classes[subclass].get_proxies(parent))

            # only one proxy should be found
            assert len(proxiesA) == 1

            # verify proper subclass was returned
            assert isinstance(proxiesA[0], classes[subclass])
            assert subclass == proxiesA[0].get("_psckey")

            # loop through the second level subclasses
            for subclassA1 in ("A1a", "A1b", "A1c"):
                # collect the proxies from this subclass
                proxiesA1 = list(classes[subclassA1].get_proxies(proxiesA[0]))

                # only one proxy should be found
                assert len(proxiesA1) == 1

                # verify proper subclass was returned
                assert isinstance(proxiesA1[0], classes[subclassA1])
                assert subclassA1 == proxiesA1[0].get("_psckey")

    def test_get_subclass_by_key(self, getMPMUDClasses):
        classes = getMPMUDClasses

        # Check the map from the base class
        assert classes["A"].get_subclass_by_key("Aa") == classes["Aa"]
        assert classes["A"].get_subclass_by_key("Ab") == classes["Ab"]
        assert classes["A"].get_subclass_by_key("Ac") == classes["Ac"]

        # In the default classes, the base doc class has None
        # as a subclass key and so is the default for all unknown
        # subclass keys
        assert classes["A"].get_subclass_by_key("A") == classes["A"]
        assert classes["A"].get_subclass_by_key("Ad") == classes["A"]

    def test_get_subclass_by_key_from_subclass(self, getMPMUDClasses):
        classes = getMPMUDClasses

        # Check the map from the base class
        assert classes["Aa"].get_subclass_by_key("Aa") == classes["Aa"]
        assert classes["Aa"].get_subclass_by_key("Ab") == classes["Ab"]
        assert classes["Aa"].get_subclass_by_key("Ac") == classes["Ac"]

        # In the default classes, the base doc class has None
        # as a subclass key and so is the default for all unknown
        # subclass keys
        assert classes["Aa"].get_subclass_by_key("A") == classes["A"]
        assert classes["Aa"].get_subclass_by_key("Ad") == classes["A"]

    def test_get_subclass_by_key_no_default(self):
        """Test get_subclass_by_key with a different class structure
        where the base class has its own proxy_subclass_key and thus
        there is no default class."""

        class LocalMongoListProxyA(mongo_objects.PolymorphicMongoListProxy):
            container_name = "proxyA"
            proxy_subclass_map = {}
            proxy_subclass_key = "A"

        class LocalMongoListProxyAa(LocalMongoListProxyA):
            proxy_subclass_key = "Aa"

        class LocalMongoListProxyAb(LocalMongoListProxyA):
            proxy_subclass_key = "Ab"

        class LocalMongoListProxyAc(LocalMongoListProxyA):
            proxy_subclass_key = "Ac"

        assert LocalMongoListProxyA.get_subclass_by_key("A") == LocalMongoListProxyA
        assert LocalMongoListProxyA.get_subclass_by_key("Aa") == LocalMongoListProxyAa
        assert LocalMongoListProxyA.get_subclass_by_key("Ab") == LocalMongoListProxyAb
        assert LocalMongoListProxyA.get_subclass_by_key("Ac") == LocalMongoListProxyAc

        # There is no default class (no class with a None subclass_key)
        # so unknown subclass keys will raise an exception
        with pytest.raises(mongo_objects.MongoObjectsPolymorphicMismatch):
            LocalMongoListProxyA.get_subclass_by_key("Ad")

        # Also check the return from a subclass
        assert LocalMongoListProxyAa.get_subclass_by_key("A") == LocalMongoListProxyA
        assert LocalMongoListProxyAa.get_subclass_by_key("Aa") == LocalMongoListProxyAa
        assert LocalMongoListProxyAa.get_subclass_by_key("Ab") == LocalMongoListProxyAb
        assert LocalMongoListProxyAa.get_subclass_by_key("Ac") == LocalMongoListProxyAc

        # There is no default class (no class with a None subclass_key)
        # so unknown subclass keys will raise an exception
        with pytest.raises(mongo_objects.MongoObjectsPolymorphicMismatch):
            LocalMongoListProxyAa.get_subclass_by_key("Ad")

    def test_get_subclass_from_doc(self, getMPMUDClasses):
        classes = getMPMUDClasses
        assert classes["A"].get_subclass_by_key("Aa") == classes["Aa"]
        assert (
            classes["A"].get_subclass_from_doc(
                {classes["A"].proxy_subclass_key_name: "Aa"}
            )
            == classes["Aa"]
        )
