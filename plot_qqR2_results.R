library(argparse)
source("qq.R")

parser <- ArgumentParser(description='plot list of comparison files')
parser$add_argument('--result_list_file',
                    help='file holding list of results')
parser$add_argument('--output_prefix',
                    help='name of output prefix')

args <- parser$parse_args(commandArgs(TRUE))

file_table <- read.table(args$result_list_file)
file_list <- file_table$V1

plot_qqR2_csvs(file_list, args$output_prefix)