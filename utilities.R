
correlate_csv_files <- function(file_1, file_2) {
	data_1 = read.csv(file_1)
	data_2 = read.csv(file_2)

	columns <- names(data_1)

	correlation = numeric(length(columns))
	samples = numeric(length(columns))
	pvalues = numeric(length(columns))
	y_min = numeric(length(columns))
	y_max = numeric(length(columns))
	index = 1
	for( i in columns ) {
		x <- data_1[[i]]
		y <- data_2[[i]]
		OK <- complete.cases(x, y)
		count <- length(OK[OK == TRUE])
		if (count > 6) {
			res = cor.test(x, y, alternative="two.sided", method="pearson",conf.level=0.95)
			pvalues[index] = res$p.value
			correlation[index] = res$estimate
			y_min[index] = res$conf.int[1]
			y_max[index] = res$conf.int[2]
		} else {
			correlation[index] = NA
		}
		samples[index] = count
		index = index+1
	}
	results <- data.frame(Columns = columns,
			Correlation = correlation, P.Value = pvalues,
			 Samples = samples, Ymin = y_min, Ymax = y_max, Rows = nrow(data_1))
}