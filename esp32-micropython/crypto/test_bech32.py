# test_bech32
import bech32


print("--- basic bech32 test ---")

lnurl = bech32.encode("lnurl", 1, b"https://someURLforLNnode")
print("lnurl: ", lnurl)
# > lnurl1pdp68gurn8ghj7um0d4j425jvvehhynzwdehkgeg0tppps