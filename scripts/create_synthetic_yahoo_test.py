num_topics = 6980
num_rerank = 1000

sample_set = []
with open("data/letor_c14b/dataset/ltrc_yahoo/yahoo.test", "r") as f:
    for i, line in enumerate(f):
        if i < num_rerank:
            sample_set.append(line)

with open("data/letor_c14b/dataset/ltrc_yahoo/yahoo.synthetic.test", "w") as f:
    for i in range(num_topics):
        f.writelines(sample_set)

with open("data/letor_c14b/dataset/ltrc_yahoo/yahoo.synthetic.test.query", "w") as f:
    for i in range(num_topics):
        f.write(f"{num_rerank}\n")

with open("data/letor_c14b/dataset/ltrc_yahoo/yahoo.synthetic.test.group", "w") as f:
    for i in range(num_topics):
        f.write(f"{num_rerank}\n")
