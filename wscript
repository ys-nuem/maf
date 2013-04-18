top = '.'
out = 'build'

def options(ctx):
    ctx.load('maf')

def configure(ctx):
    ctx.load('maf')

def build(bld):
    pass

def get_liblinear_accuracy(filename):
    '''
    liblinear-predictの標準出力が入ったファイル名を受け取ってaccuracyを返す
    '''
    l = open(filename).next()
    # Accuracy = 80.7413% (3224/3993) -> 80.7413
    # TODO(beam2d): Use JSON
    return '{"accuracy":%s}' % l.split(' ')[2][:-1]
    # return float(l.split(' ')[2][:-1])

def divide_by_row(data_lines, num_v):
    num_examples = len(data_lines)
    num_each = len(data_lines) / num_v
    range_idxs = [(i * num_each, min((i+1) * num_each, num_examples))
                  for i in range(num_v)]
    print range_idxs
    return [data_lines[b:e] for b, e in range_idxs]

def experiment(exp):
    exp.cv(task = 'supervised-learning',
        data = '/home/ken/maf/master/news20.small',
        model = 'news20-cv',
        parameters = {
            'C': ['0.1', '1', '10'], 's': ['0', '1']
            },
        num_validation = 3,
        train = exp.sh('liblinear-train -s ${s} -c ${C} ${TRAINDATA} ${MODEL}'),
        test = exp.sh('liblinear-predict ${TESTDATA} ${MODEL} /dev/null > $@',
                      postprocess=get_liblinear_accuracy),
        score = 'accuracy',
        divide_fun = divide_by_row)

    exp(features = 'train',
        task = 'supervised-learning',
        # traindata = '/home/ken/maf/master/news20.small',
        model = 'news20',
        # physical_model = '/home/ken/maf/log/hdfs/path/news20',
        parameters = {
            'C': ['0.125', '0.25', '0.5'],
            's': ['0', '1'],
            'B': ['-1'],
            'TRAINDATA': ['/home/ken/maf/master/news20.small'],
            },
        train = exp.sh('liblinear-train -s ${s} -c ${C} -B ${B} ${TRAINDATA} ${MODEL}')
        #train = 'liblinear-train -s ${s} -c ${C} -B ${B} ${TRAINDATA} ${MODEL}'
        )

    # exp(features = 'train',
    #     task = 'supervised-learning',
    #     model = 'news20-hdfs',
    #     physical_model = '',
    #     parameters = {
    #         'traindata': ['/hdfs/path/news20.small'],
    #         'C': ['0.125', '0.25', '0.5'],
    #         's': ['0'],
    #         'B': ['-1']
    #         },
    #     train = exp.sh('liblinear-train -s ${s} -c ${C} -B ${B} ${TRAINDATA} ${MODEL}'))

    exp(features = 'test',
        task = 'supervised-learning',
        model = 'news20',
        testdata = '/data/news20/news20.t',
        # testdata = '/home/ken/maf/master/news20.t.small',
        result = 'news20-result',
        test = exp.sh('liblinear-predict ${TESTDATA} ${MODEL} /dev/null > $@',
                      postprocess=get_liblinear_accuracy))

    exp(features = 'draw',
        result = 'news20-cv/0-result',
        figure = 'news20-figure',
        x_axis = {'name': 'C', 'scale': 'log'},
        y_axis = {'name': 'accuracy'},
        legend = 's')
    
    # from  maflib import Utils
    # exp(features='draw',
    #     result='news20/log',
    #     figure='news20-train-figure',
    #     x_axis={'name': 'C', 'scale': 'log'},
    #     y_axis={'name': 'time', 'converter': Utils.convert_to_minutes},
    #     legend='s')

# 2月の目標
# ユーザががんばれば次ができるレベル
#   cross validation / train/dev/test (train/devの自動分割)
#   いろんな軸で結果をvisualize
#   新しいドメインを追加できる、典型的なのはできるだけ実装済みにする
#   多クラス分類の指標いろいろ実装 (accuracy以外で, labelごとのprecision/recallなど)
#   学習途中のモデルや評価指標のトレース (学習器自体の実装にも触れる必要があるかも)
