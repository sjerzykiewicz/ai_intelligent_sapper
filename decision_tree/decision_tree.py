import pandas as pd
import dill
import math
import numpy as np


class TreeNode:
    def __init__(self):
        self.children = []
        self.value = ""
        self.isLeaf = False
        self.pred = ""


class DecisionTree:
    def __init__(self):
        data = pd.read_csv("decision_tree/input.csv")
        features = [feat for feat in data]
        features.remove("answer")

        self.root = self._id3(data, features)

        self.file_path = "decision_tree/printed_tree.txt"
        file = open(self.file_path, "w")
        file.close()
        self._printTree(self.root, 0)

    def _entropy(self, examples):
        pos = 0.0
        neg = 0.0
        for _, row in examples.iterrows():
            if row["answer"] == "defuse":
                pos += 1
            else:
                neg += 1
        if pos == 0.0 or neg == 0.0:
            return 0.0
        else:
            p = pos / (pos + neg)
            n = neg / (pos + neg)
            return -(p * math.log(p, 2) + n * math.log(n, 2))

    def _info_gain(self, examples, attr):
        uniq = np.unique(examples[attr])
        gain = self._entropy(examples)
        for u in uniq:
            subdata = examples[examples[attr] == u]
            sub_e = self._entropy(subdata)
            gain -= (float(len(subdata)) / float(len(examples))) * sub_e
        return gain

    def _id3(self, examples, attrs):
        root = TreeNode()

        max_gain = 0
        max_feat = ""
        for feature in attrs:
            gain = self._info_gain(examples, feature)
            if gain > max_gain:
                max_gain = gain
                max_feat = feature
        root.value = max_feat
        uniq = np.unique(examples[max_feat])
        for u in uniq:
            subdata = examples[examples[max_feat] == u]
            if self._entropy(subdata) == 0.0:
                newNode = TreeNode()
                newNode.isLeaf = True
                newNode.value = u
                newNode.pred = np.unique(subdata["answer"])
                root.children.append(newNode)
            else:
                dummyNode = TreeNode()
                dummyNode.value = u
                new_attrs = attrs.copy()
                new_attrs.remove(max_feat)
                child = self._id3(subdata, new_attrs)
                dummyNode.children.append(child)
                root.children.append(dummyNode)

        return root

    def _printTree(self, root: TreeNode, depth=0):
        with open(self.file_path, "a") as file:
            for _ in range(depth):
                file.write("\t")
            file.write(root.value)
            if root.isLeaf:
                file.write(" -> ")
                file.write(str(root.pred))
            file.write("\n")
        for child in root.children:
            self._printTree(child, depth + 1)

    def _classify(self, root, new):
        while len(root.children) > 0:
            for child in root.children:
                if child.value == new[root.value]:
                    if child.isLeaf:
                        root = child
                    else:
                        root = child.children[0]
                    break
        return root.pred

    def get_decision(self, new):
        return self._classify(self.root, new)


if __name__ == "__main__":
    dt = DecisionTree()
    with open("decision_tree/decision_tree.joblib", "wb") as f:
        dill.dump(dt, f)
