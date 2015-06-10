library(argparse)
source("utilities.R")
source("qq.R")

parser <- ArgumentParser(description='Process some integers')
parser$add_argument('--file1',
                    help='first file in the comparison')
parser$add_argument('--file2',
                    help='second file in the comparison')
parser$add_argument('--name',
                    help='name to tag results')
parser$add_argument('--out',
                    help='name of output')

args <- parser$parse_args(commandArgs(TRUE))

results <- correlate_csv_files(args$file1, args$file2)

R2 <- results$Correlation^2
data <- tissue_qqR2(R2, tail(results$Rows,1), args$name)
data$R2 <- R2

write.table(data, file = args$out, sep='\t', col.names = colnames(data))

