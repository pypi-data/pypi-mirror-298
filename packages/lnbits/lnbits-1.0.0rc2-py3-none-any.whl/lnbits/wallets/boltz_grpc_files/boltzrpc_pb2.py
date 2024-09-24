# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lnbits/wallets/boltz_grpc_files/boltzrpc.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n.lnbits/wallets/boltz_grpc_files/boltzrpc.proto\x12\x08\x62oltzrpc\x1a\x1bgoogle/protobuf/empty.proto"#\n\x13\x43reateTenantRequest\x12\x0c\n\x04name\x18\x01 \x01(\t"\x14\n\x12ListTenantsRequest"8\n\x13ListTenantsResponse\x12!\n\x07tenants\x18\x01 \x03(\x0b\x32\x10.boltzrpc.Tenant" \n\x10GetTenantRequest\x12\x0c\n\x04name\x18\x01 \x01(\t""\n\x06Tenant\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\t"?\n\x13MacaroonPermissions\x12(\n\x06\x61\x63tion\x18\x02 \x01(\x0e\x32\x18.boltzrpc.MacaroonAction"o\n\x13\x42\x61keMacaroonRequest\x12\x16\n\ttenant_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x32\n\x0bpermissions\x18\x02 \x03(\x0b\x32\x1d.boltzrpc.MacaroonPermissionsB\x0c\n\n_tenant_id"(\n\x14\x42\x61keMacaroonResponse\x12\x10\n\x08macaroon\x18\x01 \x01(\t"H\n\x04Pair\x12 \n\x04\x66rom\x18\x01 \x01(\x0e\x32\x12.boltzrpc.Currency\x12\x1e\n\x02to\x18\x02 \x01(\x0e\x32\x12.boltzrpc.Currency"\xf7\x04\n\x08SwapInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x1c\n\x04pair\x18\x16 \x01(\x0b\x32\x0e.boltzrpc.Pair\x12"\n\x05state\x18\x02 \x01(\x0e\x32\x13.boltzrpc.SwapState\x12\r\n\x05\x65rror\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x13\n\x0bprivate_key\x18\x05 \x01(\t\x12\x10\n\x08preimage\x18\x06 \x01(\t\x12\x15\n\rredeem_script\x18\x07 \x01(\t\x12\x0f\n\x07invoice\x18\x08 \x01(\t\x12\x16\n\x0elockup_address\x18\t \x01(\t\x12\x17\n\x0f\x65xpected_amount\x18\n \x01(\x04\x12\x1c\n\x14timeout_block_height\x18\x0b \x01(\r\x12\x1d\n\x15lockup_transaction_id\x18\x0c \x01(\t\x12\x1d\n\x15refund_transaction_id\x18\r \x01(\t\x12\x1b\n\x0erefund_address\x18\x13 \x01(\tH\x00\x88\x01\x01\x12%\n\x08\x63han_ids\x18\x0e \x03(\x0b\x32\x13.boltzrpc.ChannelId\x12\x19\n\x0c\x62linding_key\x18\x0f \x01(\tH\x01\x88\x01\x01\x12\x12\n\ncreated_at\x18\x10 \x01(\x03\x12\x18\n\x0bservice_fee\x18\x11 \x01(\x04H\x02\x88\x01\x01\x12\x18\n\x0bonchain_fee\x18\x12 \x01(\x04H\x03\x88\x01\x01\x12\x16\n\twallet_id\x18\x14 \x01(\x04H\x04\x88\x01\x01\x12\x11\n\ttenant_id\x18\x15 \x01(\x04\x42\x11\n\x0f_refund_addressB\x0f\n\r_blinding_keyB\x0e\n\x0c_service_feeB\x0e\n\x0c_onchain_feeB\x0c\n\n_wallet_id"T\n\x12GetPairInfoRequest\x12 \n\x04type\x18\x01 \x01(\x0e\x32\x12.boltzrpc.SwapType\x12\x1c\n\x04pair\x18\x02 \x01(\x0b\x32\x0e.boltzrpc.Pair"z\n\x08PairInfo\x12\x1c\n\x04pair\x18\x01 \x01(\x0b\x32\x0e.boltzrpc.Pair\x12 \n\x04\x66\x65\x65s\x18\x02 \x01(\x0b\x32\x12.boltzrpc.SwapFees\x12 \n\x06limits\x18\x03 \x01(\x0b\x32\x10.boltzrpc.Limits\x12\x0c\n\x04hash\x18\x04 \x01(\t"\xa8\x01\n\x13\x43hannelCreationInfo\x12\x0f\n\x07swap_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x19\n\x11inbound_liquidity\x18\x03 \x01(\r\x12\x0f\n\x07private\x18\x04 \x01(\x08\x12\x1e\n\x16\x66unding_transaction_id\x18\x05 \x01(\t\x12 \n\x18\x66unding_transaction_vout\x18\x06 \x01(\r:\x02\x18\x01"x\n\x17\x43ombinedChannelSwapInfo\x12 \n\x04swap\x18\x01 \x01(\x0b\x32\x12.boltzrpc.SwapInfo\x12\x37\n\x10\x63hannel_creation\x18\x02 \x01(\x0b\x32\x1d.boltzrpc.ChannelCreationInfo:\x02\x18\x01"\x91\x05\n\x0fReverseSwapInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12"\n\x05state\x18\x02 \x01(\x0e\x32\x13.boltzrpc.SwapState\x12\r\n\x05\x65rror\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x13\n\x0bprivate_key\x18\x05 \x01(\t\x12\x10\n\x08preimage\x18\x06 \x01(\t\x12\x15\n\rredeem_script\x18\x07 \x01(\t\x12\x0f\n\x07invoice\x18\x08 \x01(\t\x12\x15\n\rclaim_address\x18\t \x01(\t\x12\x16\n\x0eonchain_amount\x18\n \x01(\x03\x12\x1c\n\x14timeout_block_height\x18\x0b \x01(\r\x12\x1d\n\x15lockup_transaction_id\x18\x0c \x01(\t\x12\x1c\n\x14\x63laim_transaction_id\x18\r \x01(\t\x12\x1c\n\x04pair\x18\x0e \x01(\x0b\x32\x0e.boltzrpc.Pair\x12%\n\x08\x63han_ids\x18\x0f \x03(\x0b\x32\x13.boltzrpc.ChannelId\x12\x19\n\x0c\x62linding_key\x18\x10 \x01(\tH\x00\x88\x01\x01\x12\x12\n\ncreated_at\x18\x11 \x01(\x03\x12\x14\n\x07paid_at\x18\x17 \x01(\x03H\x01\x88\x01\x01\x12\x18\n\x0bservice_fee\x18\x12 \x01(\x04H\x02\x88\x01\x01\x12\x18\n\x0bonchain_fee\x18\x13 \x01(\x04H\x03\x88\x01\x01\x12\x1d\n\x10routing_fee_msat\x18\x14 \x01(\x04H\x04\x88\x01\x01\x12\x14\n\x0c\x65xternal_pay\x18\x15 \x01(\x08\x12\x11\n\ttenant_id\x18\x16 \x01(\x04\x42\x0f\n\r_blinding_keyB\n\n\x08_paid_atB\x0e\n\x0c_service_feeB\x0e\n\x0c_onchain_feeB\x13\n\x11_routing_fee_msat";\n\x0c\x42lockHeights\x12\x0b\n\x03\x62tc\x18\x01 \x01(\r\x12\x13\n\x06liquid\x18\x02 \x01(\rH\x00\x88\x01\x01\x42\t\n\x07_liquid"\x10\n\x0eGetInfoRequest"\x88\x03\n\x0fGetInfoResponse\x12\x0f\n\x07version\x18\t \x01(\t\x12\x0c\n\x04node\x18\n \x01(\t\x12\x0f\n\x07network\x18\x02 \x01(\t\x12\x13\n\x0bnode_pubkey\x18\x07 \x01(\t\x12\x18\n\x10\x61uto_swap_status\x18\x0b \x01(\t\x12-\n\rblock_heights\x18\x08 \x01(\x0b\x32\x16.boltzrpc.BlockHeights\x12\x18\n\x10refundable_swaps\x18\x0c \x03(\t\x12%\n\x06tenant\x18\r \x01(\x0b\x32\x10.boltzrpc.TenantH\x00\x88\x01\x01\x12\x17\n\x0f\x63laimable_swaps\x18\x0e \x03(\t\x12\x12\n\x06symbol\x18\x01 \x01(\tB\x02\x18\x01\x12\x16\n\nlnd_pubkey\x18\x03 \x01(\tB\x02\x18\x01\x12\x18\n\x0c\x62lock_height\x18\x04 \x01(\rB\x02\x18\x01\x12\x19\n\rpending_swaps\x18\x05 \x03(\tB\x02\x18\x01\x12!\n\x15pending_reverse_swaps\x18\x06 \x03(\tB\x02\x18\x01\x42\t\n\x07_tenant"L\n\x06Limits\x12\x0f\n\x07minimal\x18\x01 \x01(\x04\x12\x0f\n\x07maximal\x18\x02 \x01(\x04\x12 \n\x18maximal_zero_conf_amount\x18\x03 \x01(\x04"2\n\x08SwapFees\x12\x12\n\npercentage\x18\x01 \x01(\x01\x12\x12\n\nminer_fees\x18\x02 \x01(\x04"\x81\x01\n\x10GetPairsResponse\x12%\n\tsubmarine\x18\x01 \x03(\x0b\x32\x12.boltzrpc.PairInfo\x12#\n\x07reverse\x18\x02 \x03(\x0b\x32\x12.boltzrpc.PairInfo\x12!\n\x05\x63hain\x18\x03 \x03(\x0b\x32\x12.boltzrpc.PairInfo",\n\tMinerFees\x12\x0e\n\x06normal\x18\x01 \x01(\r\x12\x0f\n\x07reverse\x18\x02 \x01(\r">\n\x04\x46\x65\x65s\x12\x12\n\npercentage\x18\x01 \x01(\x02\x12"\n\x05miner\x18\x02 \x01(\x0b\x32\x13.boltzrpc.MinerFees"\x17\n\x15GetServiceInfoRequest"X\n\x16GetServiceInfoResponse\x12\x1c\n\x04\x66\x65\x65s\x18\x01 \x01(\x0b\x32\x0e.boltzrpc.Fees\x12 \n\x06limits\x18\x02 \x01(\x0b\x32\x10.boltzrpc.Limits"\xca\x01\n\x10ListSwapsRequest\x12%\n\x04\x66rom\x18\x01 \x01(\x0e\x32\x12.boltzrpc.CurrencyH\x00\x88\x01\x01\x12#\n\x02to\x18\x02 \x01(\x0e\x32\x12.boltzrpc.CurrencyH\x01\x88\x01\x01\x12\'\n\x05state\x18\x04 \x01(\x0e\x32\x13.boltzrpc.SwapStateH\x02\x88\x01\x01\x12\'\n\x07include\x18\x05 \x01(\x0e\x32\x16.boltzrpc.IncludeSwapsB\x07\n\x05_fromB\x05\n\x03_toB\x08\n\x06_state"\xd4\x01\n\x11ListSwapsResponse\x12!\n\x05swaps\x18\x01 \x03(\x0b\x32\x12.boltzrpc.SwapInfo\x12<\n\x11\x63hannel_creations\x18\x02 \x03(\x0b\x32!.boltzrpc.CombinedChannelSwapInfo\x12\x30\n\rreverse_swaps\x18\x03 \x03(\x0b\x32\x19.boltzrpc.ReverseSwapInfo\x12,\n\x0b\x63hain_swaps\x18\x04 \x03(\x0b\x32\x17.boltzrpc.ChainSwapInfo":\n\x0fGetStatsRequest\x12\'\n\x07include\x18\x01 \x01(\x0e\x32\x16.boltzrpc.IncludeSwaps"6\n\x10GetStatsResponse\x12"\n\x05stats\x18\x01 \x01(\x0b\x32\x13.boltzrpc.SwapStats"V\n\x11RefundSwapRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\x07\x61\x64\x64ress\x18\x02 \x01(\tH\x00\x12\x13\n\twallet_id\x18\x03 \x01(\x04H\x00\x42\r\n\x0b\x64\x65stination"\\\n\x11\x43laimSwapsRequest\x12\x10\n\x08swap_ids\x18\x01 \x03(\t\x12\x11\n\x07\x61\x64\x64ress\x18\x02 \x01(\tH\x00\x12\x13\n\twallet_id\x18\x03 \x01(\x04H\x00\x42\r\n\x0b\x64\x65stination",\n\x12\x43laimSwapsResponse\x12\x16\n\x0etransaction_id\x18\x01 \x01(\t" \n\x12GetSwapInfoRequest\x12\n\n\x02id\x18\x01 \x01(\t"\xce\x01\n\x13GetSwapInfoResponse\x12 \n\x04swap\x18\x01 \x01(\x0b\x32\x12.boltzrpc.SwapInfo\x12\x37\n\x10\x63hannel_creation\x18\x02 \x01(\x0b\x32\x1d.boltzrpc.ChannelCreationInfo\x12/\n\x0creverse_swap\x18\x03 \x01(\x0b\x32\x19.boltzrpc.ReverseSwapInfo\x12+\n\nchain_swap\x18\x04 \x01(\x0b\x32\x17.boltzrpc.ChainSwapInfo"+\n\x0e\x44\x65positRequest\x12\x19\n\x11inbound_liquidity\x18\x01 \x01(\r"L\n\x0f\x44\x65positResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\x1c\n\x14timeout_block_height\x18\x03 \x01(\r"\xfb\x01\n\x11\x43reateSwapRequest\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x04\x12\x1c\n\x04pair\x18\x02 \x01(\x0b\x32\x0e.boltzrpc.Pair\x12\x1a\n\x12send_from_internal\x18\x04 \x01(\x08\x12\x1b\n\x0erefund_address\x18\x05 \x01(\tH\x00\x88\x01\x01\x12\x16\n\twallet_id\x18\x06 \x01(\x04H\x01\x88\x01\x01\x12\x14\n\x07invoice\x18\x07 \x01(\tH\x02\x88\x01\x01\x12\x16\n\tzero_conf\x18\x08 \x01(\x08H\x03\x88\x01\x01\x42\x11\n\x0f_refund_addressB\x0c\n\n_wallet_idB\n\n\x08_invoiceB\x0c\n\n_zero_conf"\x9d\x01\n\x12\x43reateSwapResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\x17\n\x0f\x65xpected_amount\x18\x03 \x01(\x04\x12\r\n\x05\x62ip21\x18\x04 \x01(\t\x12\r\n\x05tx_id\x18\x05 \x01(\t\x12\x1c\n\x14timeout_block_height\x18\x06 \x01(\r\x12\x15\n\rtimeout_hours\x18\x07 \x01(\x02"R\n\x14\x43reateChannelRequest\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x03\x12\x19\n\x11inbound_liquidity\x18\x02 \x01(\r\x12\x0f\n\x07private\x18\x03 \x01(\x08"\xb9\x02\n\x18\x43reateReverseSwapRequest\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x04\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\x18\n\x10\x61\x63\x63\x65pt_zero_conf\x18\x03 \x01(\x08\x12\x1c\n\x04pair\x18\x04 \x01(\x0b\x32\x0e.boltzrpc.Pair\x12\x10\n\x08\x63han_ids\x18\x05 \x03(\t\x12\x16\n\twallet_id\x18\x06 \x01(\x04H\x00\x88\x01\x01\x12\x1f\n\x12return_immediately\x18\x07 \x01(\x08H\x01\x88\x01\x01\x12\x19\n\x0c\x65xternal_pay\x18\x08 \x01(\x08H\x02\x88\x01\x01\x12\x18\n\x0b\x64\x65scription\x18\t \x01(\tH\x03\x88\x01\x01\x42\x0c\n\n_wallet_idB\x15\n\x13_return_immediatelyB\x0f\n\r_external_payB\x0e\n\x0c_description"\xdb\x01\n\x19\x43reateReverseSwapResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x16\n\x0elockup_address\x18\x02 \x01(\t\x12"\n\x15routing_fee_milli_sat\x18\x03 \x01(\x04H\x00\x88\x01\x01\x12!\n\x14\x63laim_transaction_id\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07invoice\x18\x05 \x01(\tH\x02\x88\x01\x01\x42\x18\n\x16_routing_fee_milli_satB\x17\n\x15_claim_transaction_idB\n\n\x08_invoice"\x8e\x03\n\x16\x43reateChainSwapRequest\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x04\x12\x1c\n\x04pair\x18\x02 \x01(\x0b\x32\x0e.boltzrpc.Pair\x12\x17\n\nto_address\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x1b\n\x0erefund_address\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x1b\n\x0e\x66rom_wallet_id\x18\x05 \x01(\x04H\x02\x88\x01\x01\x12\x19\n\x0cto_wallet_id\x18\x06 \x01(\x04H\x03\x88\x01\x01\x12\x1d\n\x10\x61\x63\x63\x65pt_zero_conf\x18\x07 \x01(\x08H\x04\x88\x01\x01\x12\x19\n\x0c\x65xternal_pay\x18\x08 \x01(\x08H\x05\x88\x01\x01\x12\x1d\n\x10lockup_zero_conf\x18\t \x01(\x08H\x06\x88\x01\x01\x42\r\n\x0b_to_addressB\x11\n\x0f_refund_addressB\x11\n\x0f_from_wallet_idB\x0f\n\r_to_wallet_idB\x13\n\x11_accept_zero_confB\x0f\n\r_external_payB\x13\n\x11_lockup_zero_conf"\x8d\x03\n\rChainSwapInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x1c\n\x04pair\x18\x02 \x01(\x0b\x32\x0e.boltzrpc.Pair\x12"\n\x05state\x18\x03 \x01(\x0e\x32\x13.boltzrpc.SwapState\x12\r\n\x05\x65rror\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\x10\n\x08preimage\x18\x06 \x01(\t\x12\x0f\n\x07is_auto\x18\x08 \x01(\x08\x12\x18\n\x0bservice_fee\x18\t \x01(\x04H\x00\x88\x01\x01\x12\x1b\n\x13service_fee_percent\x18\n \x01(\x01\x12\x18\n\x0bonchain_fee\x18\x0b \x01(\x04H\x01\x88\x01\x01\x12\x12\n\ncreated_at\x18\x0c \x01(\x03\x12\x11\n\ttenant_id\x18\r \x01(\x04\x12*\n\tfrom_data\x18\x0e \x01(\x0b\x32\x17.boltzrpc.ChainSwapData\x12(\n\x07to_data\x18\x0f \x01(\x0b\x32\x17.boltzrpc.ChainSwapDataB\x0e\n\x0c_service_feeB\x0e\n\x0c_onchain_fee"\x98\x03\n\rChainSwapData\x12\n\n\x02id\x18\x01 \x01(\t\x12$\n\x08\x63urrency\x18\x02 \x01(\x0e\x32\x12.boltzrpc.Currency\x12\x13\n\x0bprivate_key\x18\x03 \x01(\t\x12\x18\n\x10their_public_key\x18\x04 \x01(\t\x12\x0e\n\x06\x61mount\x18\x06 \x01(\x04\x12\x1c\n\x14timeout_block_height\x18\x07 \x01(\r\x12"\n\x15lockup_transaction_id\x18\x08 \x01(\tH\x00\x88\x01\x01\x12\x1b\n\x0etransaction_id\x18\t \x01(\tH\x01\x88\x01\x01\x12\x16\n\twallet_id\x18\x14 \x01(\x04H\x02\x88\x01\x01\x12\x14\n\x07\x61\x64\x64ress\x18\x0c \x01(\tH\x03\x88\x01\x01\x12\x19\n\x0c\x62linding_key\x18\r \x01(\tH\x04\x88\x01\x01\x12\x16\n\x0elockup_address\x18\x0e \x01(\tB\x18\n\x16_lockup_transaction_idB\x11\n\x0f_transaction_idB\x0c\n\n_wallet_idB\n\n\x08_addressB\x0f\n\r_blinding_key"%\n\tChannelId\x12\x0b\n\x03\x63ln\x18\x01 \x01(\t\x12\x0b\n\x03lnd\x18\x02 \x01(\x04"\x81\x01\n\x10LightningChannel\x12\x1f\n\x02id\x18\x01 \x01(\x0b\x32\x13.boltzrpc.ChannelId\x12\x10\n\x08\x63\x61pacity\x18\x02 \x01(\x04\x12\x14\n\x0coutbound_sat\x18\x03 \x01(\x04\x12\x13\n\x0binbound_sat\x18\x04 \x01(\x04\x12\x0f\n\x07peer_id\x18\x05 \x01(\t"\x81\x01\n\tSwapStats\x12\x12\n\ntotal_fees\x18\x01 \x01(\x04\x12\x14\n\x0ctotal_amount\x18\x02 \x01(\x04\x12\x10\n\x08\x61vg_fees\x18\x03 \x01(\x04\x12\x12\n\navg_amount\x18\x04 \x01(\x04\x12\r\n\x05\x63ount\x18\x05 \x01(\x04\x12\x15\n\rsuccess_count\x18\x06 \x01(\x04"P\n\x06\x42udget\x12\r\n\x05total\x18\x01 \x01(\x04\x12\x11\n\tremaining\x18\x02 \x01(\x03\x12\x12\n\nstart_date\x18\x03 \x01(\x03\x12\x10\n\x08\x65nd_date\x18\x04 \x01(\x03"\xad\x01\n\x11WalletCredentials\x12\x15\n\x08mnemonic\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x11\n\x04xpub\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x1c\n\x0f\x63ore_descriptor\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x17\n\nsubaccount\x18\x04 \x01(\x04H\x03\x88\x01\x01\x42\x0b\n\t_mnemonicB\x07\n\x05_xpubB\x12\n\x10_core_descriptorB\r\n\x0b_subaccount"f\n\x0cWalletParams\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x08\x63urrency\x18\x02 \x01(\x0e\x32\x12.boltzrpc.Currency\x12\x15\n\x08password\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_password"o\n\x13ImportWalletRequest\x12\x30\n\x0b\x63redentials\x18\x01 \x01(\x0b\x32\x1b.boltzrpc.WalletCredentials\x12&\n\x06params\x18\x02 \x01(\x0b\x32\x16.boltzrpc.WalletParams"=\n\x13\x43reateWalletRequest\x12&\n\x06params\x18\x02 \x01(\x0b\x32\x16.boltzrpc.WalletParams"J\n\x14\x43reateWalletResponse\x12\x10\n\x08mnemonic\x18\x01 \x01(\t\x12 \n\x06wallet\x18\x02 \x01(\x0b\x32\x10.boltzrpc.Wallet"Q\n\x14SetSubaccountRequest\x12\x11\n\twallet_id\x18\x01 \x01(\x04\x12\x17\n\nsubaccount\x18\x02 \x01(\x04H\x00\x88\x01\x01\x42\r\n\x0b_subaccount"*\n\x15GetSubaccountsRequest\x12\x11\n\twallet_id\x18\x01 \x01(\x04"e\n\x16GetSubaccountsResponse\x12\x14\n\x07\x63urrent\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12)\n\x0bsubaccounts\x18\x02 \x03(\x0b\x32\x14.boltzrpc.SubaccountB\n\n\x08_current"\x16\n\x14ImportWalletResponse"\x7f\n\x11GetWalletsRequest\x12)\n\x08\x63urrency\x18\x01 \x01(\x0e\x32\x12.boltzrpc.CurrencyH\x00\x88\x01\x01\x12\x1d\n\x10include_readonly\x18\x02 \x01(\x08H\x01\x88\x01\x01\x42\x0b\n\t_currencyB\x13\n\x11_include_readonly"F\n\x10GetWalletRequest\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x0f\n\x02id\x18\x02 \x01(\x04H\x01\x88\x01\x01\x42\x07\n\x05_nameB\x05\n\x03_id"M\n\x1bGetWalletCredentialsRequest\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x15\n\x08password\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_password"!\n\x13RemoveWalletRequest\x12\n\n\x02id\x18\x01 \x01(\x04"\x91\x01\n\x06Wallet\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\t\x12$\n\x08\x63urrency\x18\x03 \x01(\x0e\x32\x12.boltzrpc.Currency\x12\x10\n\x08readonly\x18\x04 \x01(\x08\x12"\n\x07\x62\x61lance\x18\x05 \x01(\x0b\x32\x11.boltzrpc.Balance\x12\x11\n\ttenant_id\x18\x06 \x01(\x04",\n\x07Wallets\x12!\n\x07wallets\x18\x01 \x03(\x0b\x32\x10.boltzrpc.Wallet"@\n\x07\x42\x61lance\x12\r\n\x05total\x18\x01 \x01(\x04\x12\x11\n\tconfirmed\x18\x02 \x01(\x04\x12\x13\n\x0bunconfirmed\x18\x03 \x01(\x04"O\n\nSubaccount\x12"\n\x07\x62\x61lance\x18\x01 \x01(\x0b\x32\x11.boltzrpc.Balance\x12\x0f\n\x07pointer\x18\x02 \x01(\x04\x12\x0c\n\x04type\x18\x03 \x01(\t"\x16\n\x14RemoveWalletResponse"!\n\rUnlockRequest\x12\x10\n\x08password\x18\x01 \x01(\t"/\n\x1bVerifyWalletPasswordRequest\x12\x10\n\x08password\x18\x01 \x01(\t"/\n\x1cVerifyWalletPasswordResponse\x12\x0f\n\x07\x63orrect\x18\x01 \x01(\x08"7\n\x1b\x43hangeWalletPasswordRequest\x12\x0b\n\x03old\x18\x01 \x01(\t\x12\x0b\n\x03new\x18\x02 \x01(\t*%\n\x0eMacaroonAction\x12\x08\n\x04READ\x10\x00\x12\t\n\x05WRITE\x10\x01*b\n\tSwapState\x12\x0b\n\x07PENDING\x10\x00\x12\x0e\n\nSUCCESSFUL\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x12\x10\n\x0cSERVER_ERROR\x10\x03\x12\x0c\n\x08REFUNDED\x10\x04\x12\r\n\tABANDONED\x10\x05*\x1d\n\x08\x43urrency\x12\x07\n\x03\x42TC\x10\x00\x12\x08\n\x04LBTC\x10\x01*1\n\x08SwapType\x12\r\n\tSUBMARINE\x10\x00\x12\x0b\n\x07REVERSE\x10\x01\x12\t\n\x05\x43HAIN\x10\x02*-\n\x0cIncludeSwaps\x12\x07\n\x03\x41LL\x10\x00\x12\n\n\x06MANUAL\x10\x01\x12\x08\n\x04\x41UTO\x10\x02\x32\x84\x12\n\x05\x42oltz\x12>\n\x07GetInfo\x12\x18.boltzrpc.GetInfoRequest\x1a\x19.boltzrpc.GetInfoResponse\x12X\n\x0eGetServiceInfo\x12\x1f.boltzrpc.GetServiceInfoRequest\x1a .boltzrpc.GetServiceInfoResponse"\x03\x88\x02\x01\x12?\n\x0bGetPairInfo\x12\x1c.boltzrpc.GetPairInfoRequest\x1a\x12.boltzrpc.PairInfo\x12>\n\x08GetPairs\x12\x16.google.protobuf.Empty\x1a\x1a.boltzrpc.GetPairsResponse\x12\x44\n\tListSwaps\x12\x1a.boltzrpc.ListSwapsRequest\x1a\x1b.boltzrpc.ListSwapsResponse\x12\x41\n\x08GetStats\x12\x19.boltzrpc.GetStatsRequest\x1a\x1a.boltzrpc.GetStatsResponse\x12H\n\nRefundSwap\x12\x1b.boltzrpc.RefundSwapRequest\x1a\x1d.boltzrpc.GetSwapInfoResponse\x12G\n\nClaimSwaps\x12\x1b.boltzrpc.ClaimSwapsRequest\x1a\x1c.boltzrpc.ClaimSwapsResponse\x12J\n\x0bGetSwapInfo\x12\x1c.boltzrpc.GetSwapInfoRequest\x1a\x1d.boltzrpc.GetSwapInfoResponse\x12R\n\x11GetSwapInfoStream\x12\x1c.boltzrpc.GetSwapInfoRequest\x1a\x1d.boltzrpc.GetSwapInfoResponse0\x01\x12\x43\n\x07\x44\x65posit\x12\x18.boltzrpc.DepositRequest\x1a\x19.boltzrpc.DepositResponse"\x03\x88\x02\x01\x12G\n\nCreateSwap\x12\x1b.boltzrpc.CreateSwapRequest\x1a\x1c.boltzrpc.CreateSwapResponse\x12R\n\rCreateChannel\x12\x1e.boltzrpc.CreateChannelRequest\x1a\x1c.boltzrpc.CreateSwapResponse"\x03\x88\x02\x01\x12\\\n\x11\x43reateReverseSwap\x12".boltzrpc.CreateReverseSwapRequest\x1a#.boltzrpc.CreateReverseSwapResponse\x12L\n\x0f\x43reateChainSwap\x12 .boltzrpc.CreateChainSwapRequest\x1a\x17.boltzrpc.ChainSwapInfo\x12M\n\x0c\x43reateWallet\x12\x1d.boltzrpc.CreateWalletRequest\x1a\x1e.boltzrpc.CreateWalletResponse\x12?\n\x0cImportWallet\x12\x1d.boltzrpc.ImportWalletRequest\x1a\x10.boltzrpc.Wallet\x12\x45\n\rSetSubaccount\x12\x1e.boltzrpc.SetSubaccountRequest\x1a\x14.boltzrpc.Subaccount\x12S\n\x0eGetSubaccounts\x12\x1f.boltzrpc.GetSubaccountsRequest\x1a .boltzrpc.GetSubaccountsResponse\x12<\n\nGetWallets\x12\x1b.boltzrpc.GetWalletsRequest\x1a\x11.boltzrpc.Wallets\x12\x39\n\tGetWallet\x12\x1a.boltzrpc.GetWalletRequest\x1a\x10.boltzrpc.Wallet\x12Z\n\x14GetWalletCredentials\x12%.boltzrpc.GetWalletCredentialsRequest\x1a\x1b.boltzrpc.WalletCredentials\x12M\n\x0cRemoveWallet\x12\x1d.boltzrpc.RemoveWalletRequest\x1a\x1e.boltzrpc.RemoveWalletResponse\x12\x36\n\x04Stop\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\x12\x39\n\x06Unlock\x12\x17.boltzrpc.UnlockRequest\x1a\x16.google.protobuf.Empty\x12\x65\n\x14VerifyWalletPassword\x12%.boltzrpc.VerifyWalletPasswordRequest\x1a&.boltzrpc.VerifyWalletPasswordResponse\x12U\n\x14\x43hangeWalletPassword\x12%.boltzrpc.ChangeWalletPasswordRequest\x1a\x16.google.protobuf.Empty\x12?\n\x0c\x43reateTenant\x12\x1d.boltzrpc.CreateTenantRequest\x1a\x10.boltzrpc.Tenant\x12J\n\x0bListTenants\x12\x1c.boltzrpc.ListTenantsRequest\x1a\x1d.boltzrpc.ListTenantsResponse\x12\x39\n\tGetTenant\x12\x1a.boltzrpc.GetTenantRequest\x1a\x10.boltzrpc.Tenant\x12M\n\x0c\x42\x61keMacaroon\x12\x1d.boltzrpc.BakeMacaroonRequest\x1a\x1e.boltzrpc.BakeMacaroonResponseB0Z.github.com/BoltzExchange/boltz-client/boltzrpcb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "lnbits.wallets.boltz_grpc_files.boltzrpc_pb2", _globals
)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals["DESCRIPTOR"]._loaded_options = None
    _globals["DESCRIPTOR"]._serialized_options = (
        b"Z.github.com/BoltzExchange/boltz-client/boltzrpc"
    )
    _globals["_CHANNELCREATIONINFO"]._loaded_options = None
    _globals["_CHANNELCREATIONINFO"]._serialized_options = b"\030\001"
    _globals["_COMBINEDCHANNELSWAPINFO"]._loaded_options = None
    _globals["_COMBINEDCHANNELSWAPINFO"]._serialized_options = b"\030\001"
    _globals["_GETINFORESPONSE"].fields_by_name["symbol"]._loaded_options = None
    _globals["_GETINFORESPONSE"].fields_by_name[
        "symbol"
    ]._serialized_options = b"\030\001"
    _globals["_GETINFORESPONSE"].fields_by_name["lnd_pubkey"]._loaded_options = None
    _globals["_GETINFORESPONSE"].fields_by_name[
        "lnd_pubkey"
    ]._serialized_options = b"\030\001"
    _globals["_GETINFORESPONSE"].fields_by_name["block_height"]._loaded_options = None
    _globals["_GETINFORESPONSE"].fields_by_name[
        "block_height"
    ]._serialized_options = b"\030\001"
    _globals["_GETINFORESPONSE"].fields_by_name["pending_swaps"]._loaded_options = None
    _globals["_GETINFORESPONSE"].fields_by_name[
        "pending_swaps"
    ]._serialized_options = b"\030\001"
    _globals["_GETINFORESPONSE"].fields_by_name[
        "pending_reverse_swaps"
    ]._loaded_options = None
    _globals["_GETINFORESPONSE"].fields_by_name[
        "pending_reverse_swaps"
    ]._serialized_options = b"\030\001"
    _globals["_BOLTZ"].methods_by_name["GetServiceInfo"]._loaded_options = None
    _globals["_BOLTZ"].methods_by_name[
        "GetServiceInfo"
    ]._serialized_options = b"\210\002\001"
    _globals["_BOLTZ"].methods_by_name["Deposit"]._loaded_options = None
    _globals["_BOLTZ"].methods_by_name["Deposit"]._serialized_options = b"\210\002\001"
    _globals["_BOLTZ"].methods_by_name["CreateChannel"]._loaded_options = None
    _globals["_BOLTZ"].methods_by_name[
        "CreateChannel"
    ]._serialized_options = b"\210\002\001"
    _globals["_MACAROONACTION"]._serialized_start = 8747
    _globals["_MACAROONACTION"]._serialized_end = 8784
    _globals["_SWAPSTATE"]._serialized_start = 8786
    _globals["_SWAPSTATE"]._serialized_end = 8884
    _globals["_CURRENCY"]._serialized_start = 8886
    _globals["_CURRENCY"]._serialized_end = 8915
    _globals["_SWAPTYPE"]._serialized_start = 8917
    _globals["_SWAPTYPE"]._serialized_end = 8966
    _globals["_INCLUDESWAPS"]._serialized_start = 8968
    _globals["_INCLUDESWAPS"]._serialized_end = 9013
    _globals["_CREATETENANTREQUEST"]._serialized_start = 89
    _globals["_CREATETENANTREQUEST"]._serialized_end = 124
    _globals["_LISTTENANTSREQUEST"]._serialized_start = 126
    _globals["_LISTTENANTSREQUEST"]._serialized_end = 146
    _globals["_LISTTENANTSRESPONSE"]._serialized_start = 148
    _globals["_LISTTENANTSRESPONSE"]._serialized_end = 204
    _globals["_GETTENANTREQUEST"]._serialized_start = 206
    _globals["_GETTENANTREQUEST"]._serialized_end = 238
    _globals["_TENANT"]._serialized_start = 240
    _globals["_TENANT"]._serialized_end = 274
    _globals["_MACAROONPERMISSIONS"]._serialized_start = 276
    _globals["_MACAROONPERMISSIONS"]._serialized_end = 339
    _globals["_BAKEMACAROONREQUEST"]._serialized_start = 341
    _globals["_BAKEMACAROONREQUEST"]._serialized_end = 452
    _globals["_BAKEMACAROONRESPONSE"]._serialized_start = 454
    _globals["_BAKEMACAROONRESPONSE"]._serialized_end = 494
    _globals["_PAIR"]._serialized_start = 496
    _globals["_PAIR"]._serialized_end = 568
    _globals["_SWAPINFO"]._serialized_start = 571
    _globals["_SWAPINFO"]._serialized_end = 1202
    _globals["_GETPAIRINFOREQUEST"]._serialized_start = 1204
    _globals["_GETPAIRINFOREQUEST"]._serialized_end = 1288
    _globals["_PAIRINFO"]._serialized_start = 1290
    _globals["_PAIRINFO"]._serialized_end = 1412
    _globals["_CHANNELCREATIONINFO"]._serialized_start = 1415
    _globals["_CHANNELCREATIONINFO"]._serialized_end = 1583
    _globals["_COMBINEDCHANNELSWAPINFO"]._serialized_start = 1585
    _globals["_COMBINEDCHANNELSWAPINFO"]._serialized_end = 1705
    _globals["_REVERSESWAPINFO"]._serialized_start = 1708
    _globals["_REVERSESWAPINFO"]._serialized_end = 2365
    _globals["_BLOCKHEIGHTS"]._serialized_start = 2367
    _globals["_BLOCKHEIGHTS"]._serialized_end = 2426
    _globals["_GETINFOREQUEST"]._serialized_start = 2428
    _globals["_GETINFOREQUEST"]._serialized_end = 2444
    _globals["_GETINFORESPONSE"]._serialized_start = 2447
    _globals["_GETINFORESPONSE"]._serialized_end = 2839
    _globals["_LIMITS"]._serialized_start = 2841
    _globals["_LIMITS"]._serialized_end = 2917
    _globals["_SWAPFEES"]._serialized_start = 2919
    _globals["_SWAPFEES"]._serialized_end = 2969
    _globals["_GETPAIRSRESPONSE"]._serialized_start = 2972
    _globals["_GETPAIRSRESPONSE"]._serialized_end = 3101
    _globals["_MINERFEES"]._serialized_start = 3103
    _globals["_MINERFEES"]._serialized_end = 3147
    _globals["_FEES"]._serialized_start = 3149
    _globals["_FEES"]._serialized_end = 3211
    _globals["_GETSERVICEINFOREQUEST"]._serialized_start = 3213
    _globals["_GETSERVICEINFOREQUEST"]._serialized_end = 3236
    _globals["_GETSERVICEINFORESPONSE"]._serialized_start = 3238
    _globals["_GETSERVICEINFORESPONSE"]._serialized_end = 3326
    _globals["_LISTSWAPSREQUEST"]._serialized_start = 3329
    _globals["_LISTSWAPSREQUEST"]._serialized_end = 3531
    _globals["_LISTSWAPSRESPONSE"]._serialized_start = 3534
    _globals["_LISTSWAPSRESPONSE"]._serialized_end = 3746
    _globals["_GETSTATSREQUEST"]._serialized_start = 3748
    _globals["_GETSTATSREQUEST"]._serialized_end = 3806
    _globals["_GETSTATSRESPONSE"]._serialized_start = 3808
    _globals["_GETSTATSRESPONSE"]._serialized_end = 3862
    _globals["_REFUNDSWAPREQUEST"]._serialized_start = 3864
    _globals["_REFUNDSWAPREQUEST"]._serialized_end = 3950
    _globals["_CLAIMSWAPSREQUEST"]._serialized_start = 3952
    _globals["_CLAIMSWAPSREQUEST"]._serialized_end = 4044
    _globals["_CLAIMSWAPSRESPONSE"]._serialized_start = 4046
    _globals["_CLAIMSWAPSRESPONSE"]._serialized_end = 4090
    _globals["_GETSWAPINFOREQUEST"]._serialized_start = 4092
    _globals["_GETSWAPINFOREQUEST"]._serialized_end = 4124
    _globals["_GETSWAPINFORESPONSE"]._serialized_start = 4127
    _globals["_GETSWAPINFORESPONSE"]._serialized_end = 4333
    _globals["_DEPOSITREQUEST"]._serialized_start = 4335
    _globals["_DEPOSITREQUEST"]._serialized_end = 4378
    _globals["_DEPOSITRESPONSE"]._serialized_start = 4380
    _globals["_DEPOSITRESPONSE"]._serialized_end = 4456
    _globals["_CREATESWAPREQUEST"]._serialized_start = 4459
    _globals["_CREATESWAPREQUEST"]._serialized_end = 4710
    _globals["_CREATESWAPRESPONSE"]._serialized_start = 4713
    _globals["_CREATESWAPRESPONSE"]._serialized_end = 4870
    _globals["_CREATECHANNELREQUEST"]._serialized_start = 4872
    _globals["_CREATECHANNELREQUEST"]._serialized_end = 4954
    _globals["_CREATEREVERSESWAPREQUEST"]._serialized_start = 4957
    _globals["_CREATEREVERSESWAPREQUEST"]._serialized_end = 5270
    _globals["_CREATEREVERSESWAPRESPONSE"]._serialized_start = 5273
    _globals["_CREATEREVERSESWAPRESPONSE"]._serialized_end = 5492
    _globals["_CREATECHAINSWAPREQUEST"]._serialized_start = 5495
    _globals["_CREATECHAINSWAPREQUEST"]._serialized_end = 5893
    _globals["_CHAINSWAPINFO"]._serialized_start = 5896
    _globals["_CHAINSWAPINFO"]._serialized_end = 6293
    _globals["_CHAINSWAPDATA"]._serialized_start = 6296
    _globals["_CHAINSWAPDATA"]._serialized_end = 6704
    _globals["_CHANNELID"]._serialized_start = 6706
    _globals["_CHANNELID"]._serialized_end = 6743
    _globals["_LIGHTNINGCHANNEL"]._serialized_start = 6746
    _globals["_LIGHTNINGCHANNEL"]._serialized_end = 6875
    _globals["_SWAPSTATS"]._serialized_start = 6878
    _globals["_SWAPSTATS"]._serialized_end = 7007
    _globals["_BUDGET"]._serialized_start = 7009
    _globals["_BUDGET"]._serialized_end = 7089
    _globals["_WALLETCREDENTIALS"]._serialized_start = 7092
    _globals["_WALLETCREDENTIALS"]._serialized_end = 7265
    _globals["_WALLETPARAMS"]._serialized_start = 7267
    _globals["_WALLETPARAMS"]._serialized_end = 7369
    _globals["_IMPORTWALLETREQUEST"]._serialized_start = 7371
    _globals["_IMPORTWALLETREQUEST"]._serialized_end = 7482
    _globals["_CREATEWALLETREQUEST"]._serialized_start = 7484
    _globals["_CREATEWALLETREQUEST"]._serialized_end = 7545
    _globals["_CREATEWALLETRESPONSE"]._serialized_start = 7547
    _globals["_CREATEWALLETRESPONSE"]._serialized_end = 7621
    _globals["_SETSUBACCOUNTREQUEST"]._serialized_start = 7623
    _globals["_SETSUBACCOUNTREQUEST"]._serialized_end = 7704
    _globals["_GETSUBACCOUNTSREQUEST"]._serialized_start = 7706
    _globals["_GETSUBACCOUNTSREQUEST"]._serialized_end = 7748
    _globals["_GETSUBACCOUNTSRESPONSE"]._serialized_start = 7750
    _globals["_GETSUBACCOUNTSRESPONSE"]._serialized_end = 7851
    _globals["_IMPORTWALLETRESPONSE"]._serialized_start = 7853
    _globals["_IMPORTWALLETRESPONSE"]._serialized_end = 7875
    _globals["_GETWALLETSREQUEST"]._serialized_start = 7877
    _globals["_GETWALLETSREQUEST"]._serialized_end = 8004
    _globals["_GETWALLETREQUEST"]._serialized_start = 8006
    _globals["_GETWALLETREQUEST"]._serialized_end = 8076
    _globals["_GETWALLETCREDENTIALSREQUEST"]._serialized_start = 8078
    _globals["_GETWALLETCREDENTIALSREQUEST"]._serialized_end = 8155
    _globals["_REMOVEWALLETREQUEST"]._serialized_start = 8157
    _globals["_REMOVEWALLETREQUEST"]._serialized_end = 8190
    _globals["_WALLET"]._serialized_start = 8193
    _globals["_WALLET"]._serialized_end = 8338
    _globals["_WALLETS"]._serialized_start = 8340
    _globals["_WALLETS"]._serialized_end = 8384
    _globals["_BALANCE"]._serialized_start = 8386
    _globals["_BALANCE"]._serialized_end = 8450
    _globals["_SUBACCOUNT"]._serialized_start = 8452
    _globals["_SUBACCOUNT"]._serialized_end = 8531
    _globals["_REMOVEWALLETRESPONSE"]._serialized_start = 8533
    _globals["_REMOVEWALLETRESPONSE"]._serialized_end = 8555
    _globals["_UNLOCKREQUEST"]._serialized_start = 8557
    _globals["_UNLOCKREQUEST"]._serialized_end = 8590
    _globals["_VERIFYWALLETPASSWORDREQUEST"]._serialized_start = 8592
    _globals["_VERIFYWALLETPASSWORDREQUEST"]._serialized_end = 8639
    _globals["_VERIFYWALLETPASSWORDRESPONSE"]._serialized_start = 8641
    _globals["_VERIFYWALLETPASSWORDRESPONSE"]._serialized_end = 8688
    _globals["_CHANGEWALLETPASSWORDREQUEST"]._serialized_start = 8690
    _globals["_CHANGEWALLETPASSWORDREQUEST"]._serialized_end = 8745
    _globals["_BOLTZ"]._serialized_start = 9016
    _globals["_BOLTZ"]._serialized_end = 11324
# @@protoc_insertion_point(module_scope)
