## preprocessing-phishing-detector
Preprocessing data is performed to prepare the dataset before it is used in the phishing detection model. This stage aims to **improve data quality, organize the dataset, and ensure that the data is suitable for the next processing stage.**

## Steps
Several processes are carried out to ensure that the dataset is clean, consistent, and ready for further analysis. The preprocessing process consists of the following steps:

**1. Attribute Reduction**  <br>
Removing unnecessary attributes to focus on relevant data for phishing detection.
<br>

**2. Data Labeling**  <br>
Assigning each URL a label, **legitimate** or **phishing**, as the target class for classification.
<br>

**3. Data Cleaning**  <br>
Removing duplicate, invalid, or unusable data to improve dataset quality.
<br>

**4. Data Merging**  <br>
Combining data from different sources into a single dataset for further processing.
<br>

**5. Data Balancing**  <br>
Equalizing the number of legitimate and phishing samples to prevent class imbalance.
<br>

**6. Data Shuffling**  <br>
Randomizing the order of the data to prevent patterns based on the original data sequence and create a more representative dataset.

## Purpose 
This project was developed as part of my final project to fulfill the requirements for completing my undergraduate studies. This project provides a detailed implementation of the **preprocessing data** of the main [phishing-detector](https://github.com/lidyamarcelena/phishing-detector) project.

## Credit
The list of features and the file of allbrands.txt used in this project were adapted from the following research paper: **Towards Benchmark Datasets for Machine Learning Based Website Phishing Detection: An Experimental Study.** Special thanks to the researchers of this journal for providing valuable insights that supported my learning and contributed to the completion of this project.
