library(argparse)
source("qq.R")

parser <- ArgumentParser(description='Process some integers')
parser$add_argument('--results_files',
                    nargs="+",
                    help='list of files containing results')
parser$add_argument('--output',
                    help='name of output image')

args <- parser$parse_args(commandArgs(TRUE))

merged <- merge_qqR2_csvs_then_plot(args$results_files, args$output)
