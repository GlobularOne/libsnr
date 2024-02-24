"""
Module containing a class providing support for systemd networkd .network files
"""
import os as _os

from libsnr.util.payloads.systemd_unit import SystemdSectionType, SystemdConfigFileBase  as _SystemdConfigFileBase


def SYSTEMD_NETWORK_PATH(context: dict):
    """
     @brief Return the path to systemd's network directory
     @param context A dictionary containing the following keys : temp_dir - The path to the temporary directory used.
     @return str The path to systemd's network directory
    """
    return _os.path.join(context["temp_dir"], "usr", "lib", "systemd", "system")


class SystemdNetwork(_SystemdConfigFileBase,
                     root="/nonexistent",
                     base_sections=("Match", "Link", "SR_IOV",
                                    "Network", "Address", "Neighbor",
                                    "IPv6AddressLabel", "RoutingPolicyRule",
                                    "NextHop", "Route", "DHCPv4",
                                    "DHCPv6", "DHCPPrefixDelegation",
                                    "IPv6AcceptRA", "DHCPServer",
                                    "DHCPServerStaticLease",
                                    "IPv6SendRA", "IPv6Prefix",
                                    "IPv6RoutePrefix", "Bridge",
                                    "BridgeFDB", "BridgeMDB",
                                    "LLDP", "CAN", "IPoIB",
                                    "QDisc", "NetworkEmulator",
                                    "TokenBucketFilter", "PIE",
                                    "FlowQueuePIE", "StochasticFairBlue",
                                    "StochasticFairnessQueueing",
                                    "BFIFO", "PFIFO", "PFIFOHeadDrop",
                                    "PFIFOFast", "CAKE", "ControlledDelay",
                                    "DeficitRoundRobinScheduler",
                                    "DeficitRoundRobinSchedulerClass",
                                    "EnhancedTransmissionSelection",
                                    "GenericRandomEarlyDetection",
                                    "FairQueueingControlledDelay",
                                    "FairQueueing", "TrivialLinkEqualizer",
                                    "HierarchyTokenBucket",
                                    "HierarchyTokenBucketClass",
                                    "HeavyHitterFilter", "QuickFairQueueing",
                                    "QuickFairQueueingClass", "BridgeVLAN")):
    """
     @brief Class providing support for systemd networkd .network files
    """
    Match_section: SystemdSectionType = {}
    Link_section: SystemdSectionType = {}
    SR_IOV_section: SystemdSectionType = {}
    Network_section: SystemdSectionType = {}
    Address_section: SystemdSectionType = {}
    Neighbor_section: SystemdSectionType = {}
    IPv6AddressLabel_section: SystemdSectionType = {}
    RoutingPolicyRule_section: SystemdSectionType = {}
    NextHop_section: SystemdSectionType = {}
    Route_section: SystemdSectionType = {}
    DHCPv4_section: SystemdSectionType = {}
    DHCPv6_section: SystemdSectionType = {}
    DHCPPrefixDelegation_section: SystemdSectionType = {}
    IPv6AcceptRA_section: SystemdSectionType = {}
    DHCPServer_section: SystemdSectionType = {}
    DHCPServerStaticLease_section: SystemdSectionType = {}
    IPv6SendRA_section: SystemdSectionType = {}
    IPv6Prefix_section: SystemdSectionType = {}
    IPv6RoutePrefix_section: SystemdSectionType = {}
    Bridge_section: SystemdSectionType = {}
    BridgeFDB_section: SystemdSectionType = {}
    BridgeMDB_section: SystemdSectionType = {}
    LLDP_section: SystemdSectionType = {}
    CAN_section: SystemdSectionType = {}
    IPoIB_section: SystemdSectionType = {}
    QDisc_section: SystemdSectionType = {}
    NetworkEmulator_section: SystemdSectionType = {}
    TokenBucketFilter_section: SystemdSectionType = {}
    PIE_section: SystemdSectionType = {}
    FlowQueuePIE_section: SystemdSectionType = {}
    StochasticFairBlue_section: SystemdSectionType = {}
    StochasticFairnessQueueing_section: SystemdSectionType = {}
    BFIFO_section: SystemdSectionType = {}
    PFIFO_section: SystemdSectionType = {}
    PFIFOHeadDrop_section: SystemdSectionType = {}
    PFIFOFast_section: SystemdSectionType = {}
    CAKE_section: SystemdSectionType = {}
    ControlledDelay_section: SystemdSectionType = {}
    DeficitRoundRobinScheduler_section: SystemdSectionType = {}
    DeficitRoundRobinSchedulerClass_section: SystemdSectionType = {}
    EnhancedTransmissionSelection_section: SystemdSectionType = {}
    GenericRandomEarlyDetection_section: SystemdSectionType = {}
    FairQueueingControlledDelay_section: SystemdSectionType = {}
    FairQueueing_section: SystemdSectionType = {}
    TrivialLinkEqualizer_section: SystemdSectionType = {}
    HierarchyTokenBucket_section: SystemdSectionType = {}
    HierarchyTokenBucketClass_section: SystemdSectionType = {}
    HeavyHitterFilter_section: SystemdSectionType = {}
    QuickFairQueueing_section: SystemdSectionType = {}
    QuickFairQueueingClass_section: SystemdSectionType = {}
    BridgeVLAN_section: SystemdSectionType = {}
    _context: dict
    path: str
    root: str
    basename: str

    def __init__(self, context: dict, name: str):
        for extra_section in self._extra_sections:
            setattr(self, f"{extra_section}_section", dict())
        for base_section in self._base_sections:
            setattr(self, f"{base_section}_section", dict())
        self.root = SYSTEMD_NETWORK_PATH(context)
        self.path = _os.path.join(self.root, name + self.suffix)
        self.basename = _os.path.basename(self.path)
        self._context = context

    def write(self, make_dropin_dir: bool = True):
        self._write()
        if make_dropin_dir:
            _os.mkdir(_os.path.join(self.root, self.basename) + ".d")
