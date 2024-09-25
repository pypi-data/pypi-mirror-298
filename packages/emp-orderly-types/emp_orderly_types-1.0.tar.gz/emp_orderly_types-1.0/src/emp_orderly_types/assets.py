from enum import Enum
from typing import Any


class PerpetualAssetType(str, Enum):
    """An Enum of all supported Perpetual Asset Types"""

    BTC = "PERP_BTC_USDC"
    ETH = "PERP_ETH_USDC"
    WOO = "PERP_WOO_USDC"
    AVAX = "PERP_AVAX_USDC"
    MATIC = "PERP_MATIC_USDC"
    ARB = "PERP_ARB_USDC"
    INJ = "PERP_INJ_USDC"
    ORDI = "PERP_ORDI_USDC"
    SUI = "PERP_SUI_USDC"
    SOL = "PERP_SOL_USDC"
    TIA = "PERP_TIA_USDC"
    LINK = "PERP_LINK_USDC"
    OP = "PERP_OP_USDC"
    JUP = "PERP_JUP_USDC"
    STRK = "PERP_STRK_USDC"
    BLUR = "PERP_BLUR_USDC"
    WIF = "PERP_WIF_USDC"
    W = "PERP_W_USDC"  # WORMHOLE
    BNB = "PERP_BNB_USDC"
    WLD = "PERP_WLD_USDC"
    APT = "PERP_APT_USDC"
    XRP = "PERP_XRP_USDC"
    DOGE = "PERP_DOGE_USDC"
    ENA = "PERP_ENA_USDC"
    NEAR = "PERP_NEAR_USDC"
    FTM = "PERP_FTM_USDC"
    ETHFI = "PERP_ETHFI_USDC"
    OMNI = "PERP_OMNI_USDC"
    MERL = "PERP_MERL_USDC"
    BCH = "PERP_BCH_USDC"
    ONDO = "PERP_ONDO_USDC"
    REZ = "PERP_REZ_USDC"
    SEI = "PERP_SEI_USDC"
    FIL = "PERP_FIL_USDC"
    TON = "PERP_TON_USDC"
    BOME = "PERP_BOME_USDC"
    MEW = "PERP_MEW_USDC"
    BONK = "PERP_1000BONK_USDC"
    PEPE = "PERP_1000PEPE_USDC"
    NOT = "PERP_NOT_USDC"
    AR = "PERP_AR_USDC"
    BRETT = "PERP_BRETT_USDC"
    IO = "PERP_IO_USDC"
    ZRO = "PERP_ZRO_USDC"
    STG = "PERP_STG_USDC"
    BLAST = "PERP_BLAST_USDC"

    UNKNOWN = "UNKNOWN"

    @staticmethod
    def to_perp_or_unk(value, handler) -> "PerpetualAssetType":
        """
        The function `to_perp_or_unk` takes a value, tries to create a `PerpetualAssetType` object from it,
        and returns `PerpetualAssetType.UNKNOWN` if there is a `ValueError`.

        Examples:
            >>> PerpetualAssetType("PERP_ZRO_USDC")
            PerpetualAssetType.ZRO
            >>> PerpetualAssetType("????")
            PerpetualAssetType.UNKNOWN

        Args:
            value (Any): The `value` parameter in the `to_perp_or_unk` function is the input value that will be used to create a `PerpetualAssetType` object. The function will attempt to create a `PerpetualAssetType` object from this value. If the value is valid

        Returns:
            PerpetualAssetType: a `PerpetualAssetType` object
        """
        try:
            return PerpetualAssetType(value)
        except ValueError:
            return PerpetualAssetType.UNKNOWN
