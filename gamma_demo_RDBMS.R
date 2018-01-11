library(RJDBC)
library(MASS)

args <- commandArgs(TRUE)

if(length(args) != 2){
  stop("Not valid number of arguments")
}

data.table <- args[1]
data.dimension <- as.numeric(args[2])
start <- Sys.time()

className = "com.vertica.jdbc.Driver"
classPath = "/home/team14/project2/vertica-jdbc-7.2.1-0.jar"
drv <- JDBC(className, classPath, identifier.quote="`")
conn <- dbConnect(drv, "jdbc:vertica://localhost/gamma", "vertica", "12512Marlive")
query = paste("SELECT DenseGamma(i, j, v USING PARAMETERS d=",data.dimension,") OVER (PARTITION BY MOD(i,1) ORDER BY i,j) FROM ",data.table ,";",sep="")
res <- dbGetQuery(conn, query)
d <- sqrt(nrow(res))

Q<- matrix(,nrow = d-1, ncol = d-1)
Y<- matrix(,nrow = d-1, ncol = 1)

for (i in 1:d-1){
     for (j in 1:d-1){
     	index <- (i-1) * (d) + j
     	Q[i,j] <- res[index,3]
     }
     Y[i,1] <- res[i*d,3]
}

beta <- ginv(Q) %*% Y
beta