from random import randint
import math

from apprentice.working_memory.adapters.experta_.factory import \
    ExpertaSkillFactory
from apprentice.working_memory.representation import Sai
from experta import Rule, Fact, W, KnowledgeEngine, MATCH, TEST, AS, NOT

max_depth = 1

fields = ["JCommTable.R0C0", "JCommTable.R1C0", "JCommTable2.R0C0",
          "JCommTable3.R0C0", "JCommTable3.R1C0", "JCommTable4.R0C0",
          "JCommTable4.R1C0", "JCommTable5.R0C0", "JCommTable5.R1C0",
          "JCommTable6.R0C0", "JCommTable6.R1C0", "JCommTable7.R0C0",
          "JCommTable8.R0C0"]
answer_field = ['JCommTable6.R0C0', 'JCommTable6.R1C0']


def is_numeric_str(x):
    try:
        x = float(x)
        return True
    except Exception:
        return False


class CoreKnowledgeEngine(KnowledgeEngine):

    @Rule(
        Fact(id='done')
    )
    def click_done(self):
        # print('clicking done')
        return Sai(selection='done',
                   action='ButtonPressed',
                   inputs={'value': -1})

    @Rule(
        Fact(id='done')
    )
    def done(self):
        # print('clicking done')
        return Sai(selection='done',
                   action='ButtonPressed',
                   inputs={'value': '-1'})

    @Rule(
        Fact(id="JCommTable8.R0C0", contentEditable=True, value="")
    )
    def check(self):
        # print('checking box')
        return Sai(selection="JCommTable8.R0C0",
                   action='UpdateTextArea',
                   inputs={'value': "x"})

    @Rule(
        Fact(id=MATCH.id1, contentEditable=False, value=MATCH.value1),
        TEST(lambda id1, value1: id1 in fields and value1 != ""),
        Fact(id=MATCH.id2, contentEditable=False, value=MATCH.value2),
        TEST(lambda id2, value2: id2 in fields and value2 != ""),
        TEST(lambda id1, id2: id1 < id2),
        NOT(Fact(relation='equal', ele1=MATCH.id1, ele2=MATCH.id2))
    )
    def equal(self, id1, value1, id2, value2):
        new_id = "equal(%s, %s)" % (id1, id2)
        equality = value1 == value2
        # print('declaring equality', id1, id2, equality)
        self.declare(Fact(id=new_id,
                          relation='equal',
                          ele1=id1,
                          ele2=id2,
                          r_val=equality))

    @Rule(
        Fact(id='JCommTable8.R0C0', contentEditable=False, value='x'),
        Fact(id=W(), contentEditable=False, value=MATCH.value),
        TEST(lambda value: value != "" and is_numeric_str(value)),
        Fact(id=MATCH.field_id, contentEditable=True, value=W()),
        TEST(lambda field_id: field_id != 'JCommTable8.R0C0' and field_id not
             in answer_field),
    )
    def update_convert_field(self, field_id, value):
        # print('updating convert field', field_id, value)
        return Sai(selection=field_id,
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': value})

    @Rule(
        Fact(id=W(), contentEditable=False, value=MATCH.value),
        TEST(lambda value: value != "" and is_numeric_str(value)),
        Fact(id=MATCH.field_id, contentEditable=True, value=W()),
        TEST(lambda field_id: field_id != 'JCommTable8.R0C0'),
        TEST(lambda field_id: field_id in answer_field)
    )
    def update_answer_field(self, field_id, value):
        # print('updating answer field', field_id, value)
        return Sai(selection=field_id,
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': value})

    @Rule(
        Fact(id=W(), contentEditable=False, value=MATCH.value),
        TEST(lambda value: value != ""),
        Fact(id=MATCH.field_id, contentEditable=True, value="")
    )
    def update_field(self, field_id, value):
        # print('updating answer field', field_id, value)
        return Sai(selection=field_id,
                   action='UpdateTextField',
                   inputs={'value': value})

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, contentEditable=False,
                         value=MATCH.value1),
        TEST(lambda fact1: 'depth' not in fact1 or fact1['depth'] < max_depth),
        TEST(lambda value1: is_numeric_str(value1)),
        AS.fact2 << Fact(id=MATCH.id2, contentEditable=False,
                         value=MATCH.value2),
        TEST(lambda id1, id2: id1 <= id2),
        TEST(lambda fact2: 'depth' not in fact2 or fact2['depth'] < max_depth),
        TEST(lambda value2: is_numeric_str(value2)),
        NOT(Fact(operator='add', ele1=MATCH.id1, ele2=MATCH.id2))
    )
    def add(self, id1, value1, fact1, id2, value2, fact2):
        new_id = 'add(%s, %s)' % (id1, id2)

        new_value = float(value1) + float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        depth1 = 0 if 'depth' not in fact1 else fact1['depth']
        depth2 = 0 if 'depth' not in fact2 else fact2['depth']
        new_depth = 1 + max(depth1, depth2)

        # print('adding', id1, id2)

        self.declare(Fact(id=new_id,
                          operator='add',
                          ele1=id1,
                          ele2=id2,
                          contentEditable=False,
                          value=new_value,
                          depth=new_depth))

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, contentEditable=False,
                         value=MATCH.value1),
        TEST(lambda fact1: 'depth' not in fact1 or fact1['depth'] < max_depth),
        TEST(lambda value1: is_numeric_str(value1)),
        AS.fact2 << Fact(id=MATCH.id2, contentEditable=False,
                         value=MATCH.value2),
        TEST(lambda id1, id2: id1 <= id2),
        TEST(lambda fact2: 'depth' not in fact2 or fact2['depth'] < max_depth),
        TEST(lambda value2: is_numeric_str(value2)),
        NOT(Fact(operator='multiply', ele1=MATCH.id1, ele2=MATCH.id2))
    )
    def multiply(self, id1, value1, fact1, id2, value2, fact2):
        # print('multiplying', id1, id2)
        new_id = 'multiply(%s, %s)' % (id1, id2)

        new_value = float(value1) * float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        depth1 = 0 if 'depth' not in fact1 else fact1['depth']
        depth2 = 0 if 'depth' not in fact2 else fact2['depth']
        new_depth = 1 + max(depth1, depth2)

        self.declare(Fact(id=new_id,
                          operator='multiply',
                          ele1=id1,
                          ele2=id2,
                          contentEditable=False,
                          value=new_value,
                          depth=new_depth))

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, contentEditable=False,
                         value=MATCH.value1),
        TEST(lambda fact1: 'depth' not in fact1 or fact1['depth'] < max_depth),
        TEST(lambda value1: is_numeric_str(value1)),
        AS.fact2 << Fact(id=MATCH.id2, contentEditable=False,
                         value=MATCH.value2),
        TEST(lambda id1, id2: id1 <= id2),
        TEST(lambda fact2: 'depth' not in fact2 or fact2['depth'] < max_depth),
        TEST(lambda value2: is_numeric_str(value2)),
        NOT(Fact(operator='lcm', ele1=MATCH.id1, ele2=MATCH.id2))
    )
    def least_common_multiple(self, id1, value1, fact1, id2, value2, fact2):
        new_id = ' lcm({0}, {1})'.format(id1, id2)

        gcd = math.gcd(int(value1), int(value2))
        new_value = abs(int(value1) * int(value2)) // gcd
        # if new_value.is_integer():
        #     new_value = int(new_value)
        new_value = str(new_value)

        depth1 = 0 if 'depth' not in fact1 else fact1['depth']
        depth2 = 0 if 'depth' not in fact2 else fact2['depth']
        new_depth = 1 + max(depth1, depth2)

        self.declare(Fact(id=new_id,
                          operator='lcm',
                          ele1=id1,
                          ele2=id2,
                          contentEditable=False,
                          value=new_value,
                          depth=new_depth))

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, type='TextField', value=MATCH.value1),
        TEST(lambda value1: value1 != ""),
        TEST(lambda value1: len(value1) > 1),
    )
    def div10(self, id1, value1):
        new_id = 'div10({0})'.format(id1)

        new_value = float(value1) // 10
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        self.declare(Fact(id=new_id,
                          operator='div10',
                          depth=1,
                          ele1=id1,
                          contentEditable=False,
                          value=new_value))

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, type='TextField', value=MATCH.value1),
        TEST(lambda value1: value1 != "")
    )
    def addOne(self, id1, value1):
        new_id = 'addOne({0})'.format(id1)

        new_value = float(value1) + 1
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        self.declare(Fact(id=new_id,
                          operator='addOne',
                          depth=1,
                          ele1=id1,
                          contentEditable=False,
                          value=new_value))

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, type='TextField', value=MATCH.value1),
        TEST(lambda value1: value1 != "")
    )
    def append25(self, id1, value1):
        new_id = 'append25({0})'.format(id1)
        new_value = value1 + "25"
        self.declare(Fact(id=new_id,
                          operator='append25',
                          depth=1,
                          ele1=id1,
                          contentEditable=False,
                          value=new_value))

    @Rule(
        Fact(id='JCommTable.R0C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable2.R0C0', contentEditable=False, value="*"),
        Fact(id='JCommTable3.R0C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable6.R0C0', contentEditable=True)
    )
    def correct_multiply_num(self, value1, value2):
        new_value = float(value1) * float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        return Sai(selection='JCommTable6.R0C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': new_value})

    @Rule(
        Fact(id='JCommTable.R1C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable2.R0C0', contentEditable=False, value="*"),
        Fact(id='JCommTable3.R1C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable6.R1C0', contentEditable=True)
    )
    def correct_multiply_denom(self, value1, value2):
        new_value = float(value1) * float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        return Sai(selection='JCommTable6.R1C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': new_value})

    @Rule(
        Fact(id='JCommTable6.R0C0', contentEditable=False),
        Fact(id='JCommTable6.R1C0', contentEditable=False),
        Fact(id='done')
    )
    def correct_done(self):
        return Sai(selection='done',
                   action='ButtonPressed',
                   inputs={'value': -1})

    @Rule(
        Fact(id='JCommTable.R0C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable2.R0C0', contentEditable=False, value="+"),
        Fact(id='JCommTable3.R0C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable.R1C0', contentEditable=False, value=MATCH.value3),
        Fact(id='JCommTable3.R1C0', contentEditable=False, value=MATCH.value3),
        Fact(id='JCommTable6.R0C0', contentEditable=True)
    )
    def correct_add_same_num(self, value1, value2):
        new_value = float(value1) + float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        return Sai(selection='JCommTable6.R0C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': new_value})

    @Rule(
        Fact(id='JCommTable.R0C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable2.R0C0', contentEditable=False, value="+"),
        Fact(id='JCommTable3.R0C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable.R1C0', contentEditable=False, value=MATCH.value3),
        Fact(id='JCommTable3.R1C0', contentEditable=False, value=MATCH.value3),
        Fact(id='JCommTable6.R1C0', contentEditable=True)
    )
    def correct_copy_same_denom(self, value3):
        return Sai(selection='JCommTable6.R1C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': value3})

    @Rule(
        Fact(id="JCommTable.R1C0", contentEditable=False, value=MATCH.denom1),
        Fact(id="JCommTable2.R0C0", contentEditable=False, value="+"),
        Fact(id="JCommTable3.R1C0", contentEditable=False, value=MATCH.denom2),
        TEST(lambda denom1, denom2: denom1 != denom2),
        Fact(id="JCommTable8.R0C0", contentEditable=True, value="")
    )
    def correct_check(self):
        # print('checking box')
        return Sai(selection="JCommTable8.R0C0",
                   action='UpdateTextArea',
                   inputs={'value': "x"})

    @Rule(
        Fact(id='JCommTable2.R0C0', contentEditable=False, value="+"),
        Fact(id="JCommTable8.R0C0", contentEditable=False, value="x"),
        Fact(id='JCommTable.R0C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable3.R1C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable4.R1C0', contentEditable=False),
        Fact(id='JCommTable4.R0C0', contentEditable=True)
    )
    def correct_convert_num1(self, value1, value2):
        new_value = float(value1) * float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        return Sai(selection='JCommTable4.R0C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': new_value})

    @Rule(
        Fact(id='JCommTable2.R0C0', contentEditable=False, value="+"),
        Fact(id="JCommTable8.R0C0", contentEditable=False, value="x"),
        Fact(id='JCommTable.R1C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable3.R0C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable4.R0C0', contentEditable=False),
        Fact(id='JCommTable4.R1C0', contentEditable=False),
        Fact(id='JCommTable5.R1C0', contentEditable=False),
        Fact(id='JCommTable5.R0C0', contentEditable=True)
    )
    def correct_convert_num2(self, value1, value2):
        new_value = float(value1) * float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        return Sai(selection='JCommTable5.R0C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': new_value})

    @Rule(
        Fact(id='JCommTable2.R0C0', contentEditable=False, value="+"),
        Fact(id="JCommTable8.R0C0", contentEditable=False, value="x"),
        Fact(id='JCommTable.R1C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable3.R1C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable4.R1C0', contentEditable=True)
    )
    def correct_convert_denom1(self, value1, value2):
        new_value = float(value1) * float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        return Sai(selection='JCommTable4.R1C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': new_value})

    @Rule(
        Fact(id='JCommTable2.R0C0', contentEditable=False, value="+"),
        Fact(id="JCommTable8.R0C0", contentEditable=False, value="x"),
        Fact(id='JCommTable.R1C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable3.R1C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable4.R1C0', contentEditable=False),
        Fact(id='JCommTable5.R1C0', contentEditable=True)
    )
    def correct_convert_denom2(self, value1, value2):
        new_value = float(value1) * float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        return Sai(selection='JCommTable5.R1C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': new_value})

    @Rule(
        Fact(id='JCommTable4.R0C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable4.R1C0', contentEditable=False, value=MATCH.value3),
        Fact(id='JCommTable7.R0C0', contentEditable=False, value="+"),
        Fact(id='JCommTable5.R0C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable5.R1C0', contentEditable=False, value=MATCH.value3),
        Fact(id='JCommTable6.R0C0', contentEditable=True),
    )
    def correct_add_convert_num(self, value1, value2):
        new_value = float(value1) + float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        return Sai(selection='JCommTable6.R0C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': new_value})

    @Rule(
        Fact(id='JCommTable4.R0C0', contentEditable=False, value=MATCH.value1),
        Fact(id='JCommTable4.R1C0', contentEditable=False, value=MATCH.value3),
        Fact(id='JCommTable7.R0C0', contentEditable=False, value="+"),
        Fact(id='JCommTable5.R0C0', contentEditable=False, value=MATCH.value2),
        Fact(id='JCommTable5.R1C0', contentEditable=False, value=MATCH.value3),
        Fact(id='JCommTable6.R1C0', contentEditable=True),
    )
    def correct_copy_convert_denom(self, value3):
        return Sai(selection='JCommTable6.R1C0',
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   inputs={'value': value3})


ke = CoreKnowledgeEngine()
skill_factory = ExpertaSkillFactory(ke)

# for prop in dir(ke):
#     attr = getattr(ke, prop, None)
#     if not isinstance(attr, Rule):
#         continue
#     print(attr.__name__)
experta_skill_map = {getattr(ke, prop, None).__name__: skill_factory.from_ex_rule(getattr(ke, prop, None))
                      for prop in dir(ke) if isinstance(getattr(ke, prop, None), Rule)}


# click_done_skill = skill_factory.from_ex_rule(ke.click_done)
# check_skill = skill_factory.from_ex_rule(ke.check)
# equal_skill = skill_factory.from_ex_rule(ke.equal)
# update_answer_field_skill = skill_factory.from_ex_rule(ke.update_answer_field)
# update_convert_field_skill = skill_factory.from_ex_rule(
#     ke.update_convert_field)
# add_skill = skill_factory.from_ex_rule(ke.add)
# multiply_skill = skill_factory.from_ex_rule(ke.multiply)
# least_common_multiple = skill_factory.from_ex_rule(ke.least_common_multiple)

# correct_multiply_num = skill_factory.from_ex_rule(ke.correct_multiply_num)
# correct_multiply_denom = skill_factory.from_ex_rule(ke.correct_multiply_denom)

# correct_add_same_num = skill_factory.from_ex_rule(ke.correct_add_same_num)
# correct_copy_same_denom = skill_factory.from_ex_rule(
#     ke.correct_copy_same_denom)

# correct_check = skill_factory.from_ex_rule(ke.correct_check)
# correct_convert_num1 = skill_factory.from_ex_rule(ke.correct_convert_num1)
# correct_convert_num2 = skill_factory.from_ex_rule(ke.correct_convert_num2)
# correct_convert_denom1 = skill_factory.from_ex_rule(ke.correct_convert_denom1)
# correct_convert_denom2 = skill_factory.from_ex_rule(ke.correct_convert_denom2)
# correct_add_convert_num = skill_factory.from_ex_rule(
#     ke.correct_add_convert_num)
# correct_copy_convert_denom = skill_factory.from_ex_rule(
#     ke.correct_copy_convert_denom)

# correct_done = skill_factory.from_ex_rule(ke.correct_done)

# experta_skill_map = {'click_done': click_done_skill, 'check': check_skill,
#                       'update_answer': update_answer_field_skill,
#                       'update_convert': update_convert_field_skill,
#                       'equal': equal_skill,
#                       'add': add_skill,
#                       'multiply': multiply_skill,
#                       'least_common_multiple': least_common_multiple,

#                       'correct_multiply_num': correct_multiply_num,
#                       'correct_multiply_denom': correct_multiply_denom,
#                       'correct_done': correct_done,
#                       'correct_add_same_num': correct_add_same_num,
#                       'correct_copy_same_denom': correct_copy_same_denom,
#                       'correct_check': correct_check,
#                       'correct_convert_num1': correct_convert_num1,
#                       'correct_convert_num2': correct_convert_num2,
#                       'correct_convert_denom1': correct_convert_denom1,
#                       'correct_convert_denom2': correct_convert_denom2,
#                       'correct_add_convert_num': correct_add_convert_num,
#                       'correct_copy_convert_denom': correct_copy_convert_denom
#                       }
# from pprint import pprint

# pprint(experta_skill_map)
# skill_set = { prop:skill_factory.from_ex_rule(getattr(ke,prop,None)) for prop in dir(ke)}


class RandomFracEngine(KnowledgeEngine):

    @Rule(
        Fact(id=MATCH.id, contentEditable=True, value=W())
    )
    def input_random(self, id):
        return Sai(selection=id, action='UpdateTextArea',
                   inputs={'value': str(randint(0, 100))})

    @Rule(
        Fact(id='done')
    )
    def click_done(self):
        return Sai(selection='done', action='ButtonPressed',
                   inputs={'value': -1})


def fact_from_dict(f):
    if '__class__' in f:
        fact_class = f['__class__']
    else:
        fact_class = Fact
    f2 = {k: v for k, v in f.items() if k[:2] != "__"}
    return fact_class(f2)


if __name__ == "__main__":
    from apprentice.working_memory import ExpertaWorkingMemory
    import copy
    # from pprint import pprint
    # for prop in dir(ke):
    #     attr = getattr(ke, prop, None)
    #     if not isinstance(attr, Rule):
    #         continue
    #     print(attr.__name__)

    # c = copy.deepcopy(experta_skill_map['click_done'])
    prior_skills = [experta_skill_map['click_done']]
    prior_skills = None
    # wm = ExpertaWorkingMemory(ke=KnowledgeEngine())
    # wm.add_skills(prior_skills)
    # import collections.OrderedDict
    if prior_skills is None:
        prior_skills = {
            "click_done": False,  # True,
            "check": False,  # True,
            "equal": False,
            "update_answer": True,
            "update_convert": False,  # , True,
            "add": False,  # True,
            "multiply": False  # , True,
        }

    wm = ExpertaWorkingMemory(ke=KnowledgeEngine())

    skill_map = experta_skill_map
    prior_skills = [
        skill_map[s]
        for s, active in prior_skills.items()
        if active and s in skill_map
    ]
    wm.add_skills(prior_skills)

    temp = wm.ke.matcher
    # wm.ke.matcher = None

    c = copy.deepcopy(wm)
    wm.ke.matcher = temp

    # self.ke.matcher.__init__(self.ke)
    # self.ke.reset()
    # ftn = wm.ke.matcher.root_node.children[0]
    # cb = ftn.callback
    # copy.deepcopy(cb)
