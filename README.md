# 統計検定準1級 学習用シミュレーション環境

統計検定準1級の学習をサポートするためのJupyterノートブック集です。統計学実践ワークブックの全32章に対応し、各章のキーコンセプトの説明、Pythonによるシミュレーション、可視化、練習問題を含みます。

## セットアップ

```bash
# 依存パッケージのインストール
pip install -r requirements.txt

# Jupyter Notebookの起動
jupyter notebook
```

## ノートブック一覧

### 確率と確率分布の基礎（第1-7章）

| 章 | ファイル名 | 内容 |
|----|-----------|------|
| 1 | `01_events_and_probability.ipynb` | 事象と確率、条件付き確率、ベイズの定理 |
| 2 | `02_probability_distribution_generating_functions.ipynb` | 確率分布と母関数 |
| 3 | `03_distribution_characteristics.ipynb` | 分布の特性値（期待値、分散、歪度、尖度） |
| 4 | `04_variable_transformation.ipynb` | 変数変換、ヤコビアン、順序統計量 |
| 5 | `05_discrete_distributions.ipynb` | 離散型分布（二項、ポアソン、幾何など） |
| 6 | `06_continuous_distributions.ipynb` | 連続型分布と標本分布 |
| 7 | `07_limit_theorems.ipynb` | 極限定理と漸近理論（大数の法則、中心極限定理） |

### 統計的推定と検定（第8-13章）

| 章 | ファイル名 | 内容 |
|----|-----------|------|
| 8 | `08_statistical_estimation_basics.ipynb` | 統計的推定の基礎（MLE、モーメント法） |
| 9 | `09_interval_estimation.ipynb` | 区間推定 |
| 10 | `10_hypothesis_testing_basics.ipynb` | 検定の基礎と検定法の導出 |
| 11 | `11_normal_distribution_tests.ipynb` | 正規分布に関する検定 |
| 12 | `12_general_distribution_tests.ipynb` | 一般の分布に関する検定法 |
| 13 | `13_nonparametric_methods.ipynb` | ノンパラメトリック法 |

### 確率過程（第14-15章）

| 章 | ファイル名 | 内容 |
|----|-----------|------|
| 14 | `14_markov_chains.ipynb` | マルコフ連鎖 |
| 15 | `15_stochastic_processes.ipynb` | 確率過程の基礎（ポアソン過程、ブラウン運動） |

### 回帰分析（第16-19章）

| 章 | ファイル名 | 内容 |
|----|-----------|------|
| 16 | `16_multiple_regression.ipynb` | 重回帰分析 |
| 17 | `17_regression_diagnostics.ipynb` | 回帰診断法 |
| 18 | `18_qualitative_regression.ipynb` | 質的回帰（ロジスティック回帰） |
| 19 | `19_other_regression.ipynb` | 回帰分析その他（Ridge、LASSO） |

### 分散分析と標本調査（第20-21章）

| 章 | ファイル名 | 内容 |
|----|-----------|------|
| 20 | `20_anova_experimental_design.ipynb` | 分散分析と実験計画法 |
| 21 | `21_sampling_methods.ipynb` | 標本調査法 |

### 多変量解析（第22-26章）

| 章 | ファイル名 | 内容 |
|----|-----------|------|
| 22 | `22_pca.ipynb` | 主成分分析 |
| 23 | `23_discriminant_analysis.ipynb` | 判別分析 |
| 24 | `24_cluster_analysis.ipynb` | クラスター分析 |
| 25 | `25_factor_analysis.ipynb` | 因子分析・グラフィカルモデル |
| 26 | `26_other_multivariate.ipynb` | その他の多変量解析手法 |

### 応用トピック（第27-32章）

| 章 | ファイル名 | 内容 |
|----|-----------|------|
| 27 | `27_time_series.ipynb` | 時系列解析 |
| 28 | `28_contingency_tables.ipynb` | 分割表 |
| 29 | `29_missing_data.ipynb` | 不完全データの統計処理 |
| 30 | `30_model_selection.ipynb` | モデル選択（AIC、BIC、交差検証） |
| 31 | `31_bayesian_methods.ipynb` | ベイズ法 |
| 32 | `32_simulation.ipynb` | シミュレーション（モンテカルロ、MCMC） |

## この先 — ML への接続

本リポジトリで学んだ数理統計が実際にどこで使われるかは、
別リポジトリ [`machine-learning-playground`](https://github.com/yuzuponikemi/machine-learning-playground)
（165本）に対応表があります。

- **対応表**: `machine-learning-playground/STATS_PREREQUISITES.md`
  - 本リポジトリの32章 → それを使う ML の章／準1級より深く扱っている章
  - 逆引き（ML の章が前提とする統計の章）
- **2つは補完関係です**。準1級の主要トピック25語を playground 側で検索すると
  **23語がヒット0**（検定・分散分析・判別分析・因子分析・分割表・区間推定・ベイズ推論など）。
  **受験準備には本リポジトリだけで足ります。**

### 学び終えた後に読むと意味が変わる章

| 本リポジトリ | その後に読む ML 側 | 何が変わるか |
|---|---|---|
| **4章 変数変換・ヤコビアン** | playground 190 → 191 → 192 | ヤコビアンが「計算できるか」でモデルの設計が決まる。$O(d^3)$ を避けて三角行列にする、連続時間でトレースに変える |
| **8章 統計的推定（MLE）** | playground 196 | 生成モデルが「尤度を厳密に出せる／下界しか出ない／出せない」で分類される |
| **14章 マルコフ連鎖** | playground 194 | 「理論上は定常分布に収束する」と「実際に混合する」が全く違うことが測れる |
| **15章 確率過程（ブラウン運動）** | playground 194 → 195 | ブラウン運動の離散化が拡散モデルそのもの。ノイズ予測が $-\sqrt{1-\bar\alpha}\,\nabla\log p$ であることを係数込みで検証 |
| **22章 主成分分析** | playground 308（GANSpace） | PCA を生成モデルの潜在空間に当てて意味のある編集方向を教師なしで見つける |
| **25章 因子分析** | playground 304 | 「独立な因子に分解する」の深層版（$\beta$-VAE と定量評価） |
| **31章 ベイズ法** | playground 37-38 → 196 | VAE は変分ベイズそのもの。近似の「緩さ」が 0.0961 nats と数値で測れる |
| **32章 シミュレーション** | playground 190（逆変換法）→ 193（重点サンプリング）→ 194（MCMC） | 教科書の手法が高次元で壊れる場所と、その測り方 |

### 逆に、ML 側からこのリポジトリを引くとき

playground の章で数式が追えないときは、`STATS_PREREQUISITES.md` の「逆引き」表から
本リポジトリの該当章に戻れます。よく使われるのは
**4章（変数変換）・8章（最尤推定）・15章（確率過程）・30章（モデル選択）**です。

---

## 各ノートブックの構成

各ノートブックは以下の構成になっています：

1. **学習目標** - その章で習得すべき内容
2. **キーコンセプト** - 重要な概念と数式（LaTeX）
3. **Pythonシミュレーション** - 概念を実際に動かして理解
4. **可視化** - matplotlib/seabornによるグラフ
5. **練習問題** - 理解度確認のための問題と解答

## 必要なライブラリ

- numpy
- scipy
- pandas
- matplotlib
- seaborn
- plotly
- statsmodels
- scikit-learn
- jupyter
- ipywidgets

## 使い方

1. 各章を順番に進めることをお勧めします
2. 数式を読んで理論を理解した後、コードを実行してシミュレーションを確認
3. 練習問題を解いて理解度をチェック
4. 必要に応じてパラメータを変更して実験

## 参考文献

- 日本統計学会編『統計学実践ワークブック』学術図書出版社
- 統計検定公式サイト: https://www.toukei-kentei.jp/

## ライセンス

MIT License
