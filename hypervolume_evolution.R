# rm(list = ls(all = TRUE))
setwd("~/MOEADr/R/")
library(MOEADr)
library(emoa)
library(ggplot2)

# names of algorithms in analysis
names <- c("no_adaptation",
	   "no_sa",
	   "no_w",
           "adaptation")

checkpoints <- (0:25) * 2400

seed = 0
repetitions = 10


# for (i in 9:9) {
#   fun.names1[[length(fun.names1) + 1]] = paste0("UF", i)
# }
fun.names1 <- list()
for (i in 1:7) {
  fun.names1[[length(fun.names1) + 1]] = paste0("DTLZ", i)
}

#function for loading pareto fronts data
loadPlotData <- function (iter, wd = '~/dataExp/') {
  Y <-
    read.csv(paste0(wd, iter, '_paretos.csv'),
             sep = " ",
             header = F)[, 0:n_obj]
  temp <-
    read.csv(paste0(wd, iter, '_info_gen.csv'),
             sep = " ",
             header = F)
  
  out <- list(Y           = Y,
              nfe         = temp[1, ],
              n.iter      = temp[2, ])
  return(out)
}

getminP <- function(X) {
  apply(X,
        MARGIN = 2,
        FUN = min,
        na.rm = TRUE)
}

getmaxP <- function(X) {
  apply(X,
        MARGIN = 2,
        FUN = max,
        na.rm = TRUE)
}

scaling_Y <- function(Y, X) {
  minP <- getminP(rbind(Y, X))
  maxP <- getmaxP(rbind(Y, X))
  
  MinP <- matrix(rep(minP, times = nrow(Y)),
                 nrow  = nrow(Y),
                 byrow = TRUE)
  MaxP <- matrix(rep(maxP, times = nrow(Y)),
                 nrow  = nrow(Y),
                 byrow = TRUE)
  
  # Perform linear scaling
  Y    <- (Y - MinP) / (MaxP - MinP + 1e-16)
  return (Y)
}

for (fun in fun.names1) {
  ref1 <- data.frame()
  print(fun)
  
  benchmark <- strsplit(fun, "[0-9]")[[1]][1]
  number <- strsplit(fun, "[A-Z]")[[1]][3]
  if (benchmark == "DTLZ") {
    Yref <-
      as.matrix(read.table(paste0(
        "../inst/extdata/pf_data/", fun, ".2D.pf"
      )))
    colnames(Yref) <- c("f1", "f2")
    ref.point <- c(1, 1)
    n_obj <- 2
  }
  else {
    Yref <-
      as.matrix(read.table(paste0(
        "../inst/extdata/pf_data/", fun, ".dat"
      )))
    if (as.numeric(number) == 8 ||
        as.numeric(number) == 9 || as.numeric(number) == 10) {
      colnames(Yref) <- c("f1", "f2", "f3")
      ref.point <- c(1, 1, 1)
      n_obj <- 3
    }
    else{
      colnames(Yref) <- c("f1", "f2")
      ref.point <- c(1, 1)
      n_obj <- 2
    }
  }
  
  
  
  
  
  
  # loading pareto fronts from all outputs of the exp for analysis - for HV scaling
  for (i in seed:(seed + repetitions)) {
    for (name in names) {
      # loop trough algorithms in analysis
      moea = loadPlotData(
        i,
        paste0(
          "~/../../../Volumes/HD-PNFU3/temp_exp/",
          name,
          "/final/",
          tolower(fun),
          "_"
        )
      )
      ref1 <-
        rbind(ref1,
              moea$Y)
    }
  }
  
  
  # calculating HV
  fun_hv <- data.frame()
  for (name in names) {
    # loop trough algorithms in analysis
    total_hv <- data.frame()
    for (i in seed:(seed + repetitions)) {
      moea <- loadPlotData(
        i,
        paste0(
          "~/../../../Volumes/HD-PNFU3/temp_exp/",
          name,
          "/final/",
          tolower(fun),
          "_"
        )
      )
      n.iter <- as.integer(moea$n.iter)
      my_hv <- data.frame()
      my_sum <- 0
      ck_idx <- 1
      for (j in 1:n.iter) {
        output = loadPlotData(
          j,
          paste0(
            "~/../../../Volumes/HD-PNFU3/temp_exp/",
            name,
            "/history/",
            tolower(fun),
            "_",
            i,
            "/"
          )
        )
        if (output$nfe >= checkpoints[ck_idx]) {
          # PF <- output$Y
          # nndom.idx <- find_nondominated_points(PF)
          PF <- scaling_Y(output$Y, ref1)
          hv <- dominated_hypervolume(t(PF), ref = ref.point)
          my_hv <-
            rbind(my_hv, cbind(hv = hv, iter = checkpoints[ck_idx]))
          ck_idx <- ck_idx + 1
        }
      }
      total_hv <- rbind(total_hv, my_hv)
    }
    
    fun_hv <-
      rbind(fun_hv, cbind(total_hv, strategy = name))
  }
  
  median <-
    aggregate(fun_hv$hv, median, by = list(fun_hv$strategy, fun_hv$iter))
  sd <-
    aggregate(fun_hv$hv, sd, by = list(fun_hv$strategy, fun_hv$iter))
  plot_data <- (data.frame(median, sd))
  plot_data <- plot_data[,-c(4, 5)]
  colnames(plot_data) <- c("PF_NUMBER", "iter", "median", "sd")
  plot_data$ymax <- plot_data$median + plot_data$sd
  plot_data$ymin <- plot_data$median - plot_data$sd
  
  v <- ggplot(data = plot_data,
              aes(
                x = iter,
                y = median,
                group = PF_NUMBER,
                color = PF_NUMBER,
                fill = PF_NUMBER
              )) +
    geom_point(aes(color = PF_NUMBER)) + theme_minimal() +
    geom_line(aes(color = PF_NUMBER)) +
    geom_ribbon(aes(ymin = ymax, ymax = ymin),
                alpha = .2,
                linetype = 0) +
    theme(
      legend.text = element_text(size =
                                   16),
      axis.text = element_text(size =
                                 24),
      axis.title =
        element_text(size = 26)
    )  +
    labs(
      title = fun,
      x = "Number of Function Evalutions",
      y = "HV",
      main = fun
    )
  
  print(v)
  filename = paste0("~/adaptation/", fun , name, "hv_evolution.png")
  ggsave(filename = filename,
         dpi = 600,
         width = 9)
  
  
  boxplot.data = fun_hv[fun_hv$iter == max(fun_hv$iter),]
  u <- ggplot(data = boxplot.data,
              aes(
                x = strategy,
                y = hv,
                group = strategy,
                color = strategy,
                fill = strategy
              )) +
    geom_boxplot(aes(color = strategy)) + theme_minimal()
  print(u)
  filename = paste0("~/adaptation/", fun , "hv_boxplot.png")
  ggsave(filename = filename,
         dpi = 600,
         width = 9)
}
