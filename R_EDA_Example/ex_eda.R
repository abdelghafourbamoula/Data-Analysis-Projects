help(faithful)
data(faithful)
attach(faithful)
summary(eruptions)
fivenum(eruptions) # résumé à 5 nombres de Tukey

> mean(eruptions)
> median(eruptions)
> min(eruptions)
> range(eruptions)
> quantile(eruptions)
> var(eruptions) # variance
> sqrt(var(eruptions)) # écart type