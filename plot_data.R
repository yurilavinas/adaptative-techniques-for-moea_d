# rm(list = ls(all = TRUE))
setwd("~/MOEADr/R/")
library(MOEADr)
library(emoa)
library(ggplot2)

# # names of algorithms in analysis
names <- c("no_adaptation",
	   "no_w",
	   "no_sa",
           "adaptation")
# names <- c("tmp")


seed = 0
repetitions = 9

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
  
  colnames(Y) <- c("f1", "f2")
  
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
  for (i in 0:repetitions) {
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
      # plot(moea$Y)
    }
  }
  colnames(ref1) <- c("f1", "f2")
  ref1 <-
    rbind(ref1,
          Yref)
  
  adaptation = loadPlotData(
    seed,
    paste0(
      "~/../../../Volumes/HD-PNFU3/temp_exp/",
      "adaptation",
      "/final/",
      tolower(fun),
      "_"
    )
  )
  no_adaptation = loadPlotData(
    i,
    paste0(
      "~/../../../Volumes/HD-PNFU3/temp_exp/",
      "no_adaptation",
      "/final/",
      tolower(fun),
      "_"
    )
  )
  no_w = loadPlotData(
     i,
     paste0(
       "~/../../../Volumes/HD-PNFU3/temp_exp/",
       "no_w",
       "/final/",
       tolower(fun),
       "_"
     )
   )
  no_sa = loadPlotData(
	i,
	paste0(
	"~/../../../Volumes/HD-PNFU3/temp_exp/",
	"no_w",
	"/final/",
	tolower(fun),
	"_"
    )
)

  idx <- ecr::nondominated(t(adaptation$Y))
  adaptation$scaledY <- adaptation$Y[idx,]

  idx <- ecr::nondominated(t(no_adaptation$Y))
  no_adaptation$scaledY <- no_adaptation$Y[idx,]

  idx <- ecr::nondominated(t(no_w$Y))
  no_w$scaledY <- no_w$Y[idx,]

  idx <- ecr::nondominated(t(no_sa$Y))
  no_sa$scaledY <- no_sa$Y[idx,]  

  plot_data <-
    rbind(
      data.frame(scaling_Y(Yref, ref1), Strategy = "Theoretical Pareto Front"),
      data.frame(scaling_Y(no_w$scaledY, ref1), Strategy = "NO AWA"),
      data.frame(scaling_Y(adaptation$scaledY, ref1), Strategy = "adaptation"),
      data.frame(scaling_Y(no_adaptation$scaledY, ref1), Strategy = "no_adaptation"),
      data.frame(scaling_Y(no_sa$scaledY, ref1), Strategy = "NO SA")
      # data.frame((tmp$Y), Strategy = "tmp")
      # data.frame((adaptation$Y), Strategy = "adaptation"),
      # data.frame((no_adaptation$Y), Strategy = "no_adaptation")
    )
  
  print(ggplot(plot_data, aes(f1, f2)) + geom_point(aes(color = Strategy, shape = Strategy)))
  
  
   filename = paste0("~/adaptation/", fun , "_pf.png")
   ggsave(filename = filename,
          dpi = 600,
          width = 9)
}
