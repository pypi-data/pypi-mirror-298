def compare_files(file1, file2, comment="#"):
    with open(file1) as f1:
        lines1 = f1.readlines()
    with open(file2) as f2:
        lines2 = f2.readlines()
    assert len(lines1) == len(lines2)
    for l1, l2 in zip(lines1, lines2):
        print(l1, l2)
        if l1.startswith(comment) and l2.startswith(comment):
            pass
        else:
            print(l1, l2)
            assert l1.strip() == l2.strip()


def compare_geo_files(file1, file2, comment="#"):
    with open(file1) as f1:
        lines1 = f1.readlines()
    with open(file2) as f2:
        lines2 = f2.readlines()
    assert len(lines1) == len(lines2)
    for l1, l2 in zip(lines1, lines2):
        if l1.startswith(comment) and l2.startswith(comment):
            pass
        else:
            s_l1 = l1.split()
            s_l2 = l2.split()
            print(l1, l2)
            assert len(s_l1) == len(s_l2)
            if len(s_l1) > 0 and len(s_l2) > 0:
                assert s_l1[0] == s_l2[0]
                assert float(s_l1[1]) == float(s_l1[1])
                assert float(s_l1[2]) == float(s_l1[2])
                assert float(s_l1[3]) == float(s_l1[3])
                if len(s_l1) > 4:
                    assert s_l1[4] == s_l1[4]


def compare_data_files(file1, file2, comment="#"):
    with open(file1) as f1:
        lines1 = f1.readlines()
    with open(file2) as f2:
        lines2 = f2.readlines()
    for l1, l2 in zip(lines1, lines2):
        print(l1, l2)
        if l1.startswith(comment) and l2.startswith(comment):
            pass
        else:
            s_l1 = l1.split()
            s_l2 = l2.split()
            for i1, i2 in zip(s_l1, s_l2):
                assert round(float(i1), 9) == round(float(i2), 9)
