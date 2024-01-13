D0 = {}
D1_1_1 = {"key1_depth1":"value1"}
D1_3_1 = {"key1_depth1":"value1", "key2_depth1":"value2", "key3_depth1":"value3"}
D3_3_0 = {"key1_depth3":"value1","key2_depth3":"value2","key3_depth3":"value3"}
D2_3_0 = {"key1_depth2":"value1","key2_depth2":"value2","key3_depth2":D3_3_0}
D1_1_2 = {"key1_depth1":D0}
D1_3_3 = {"key1_depth1":"value1", "key2_depth1":"value2", "key3_depth1":D2_3_0}
acc = {}
new = dict(**acc)
new.update(D1_3_1)
#.update(D1_3_1)
print(D1_1_1)
print(new)