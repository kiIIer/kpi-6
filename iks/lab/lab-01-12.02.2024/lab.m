load xy.dat

x = xy(:,1)
y = xy(:,2)

p1 = polyfit(x, y, 1)

p3 = polyfit(x, y, 3)

p5 = polyfit(x, y, 5)

xes = linspace(x(1), x(end), 100)

yes1 = polyval(p1, xes)

yes3 = polyval(p3, xes)

yes5 = polyval(p5, xes)

plot(x, y, 'o', xes, yes1, xes, yes3, xes, yes5)

yfit1 = polyval(p1, x)
yfit3 = polyval(p3, x)
yfit5 = polyval(p5, x)
yres1 = y - yfit1
yres3 = y - yfit3
yres5 = y - yfit5

Sres1 = sum(yres1.^2)
Sres3 = sum(yres3.^2)
Sres5 = sum(yres5.^2)

Stotal = (length(y)-1) * var(y)

rsq1 = 1 - Sres1/Stotal
rsq3 = 1 - Sres3/Stotal
rsq5 = 1 - Sres5/Stotal