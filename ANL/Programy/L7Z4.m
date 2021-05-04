function L=L7Z4(n)
  xi = -1:(2/n):1;
  k = length(xi);
  x = -1:0.01:1;
  f = (x-xi(1));
  for i=2:k
    f = f.*(x-xi(i));
  endfor
  
  T0 = 1;
  T1 = x;
  for i=2:n
    T = T1.*(2*x) - T0;
    T0 = T1;
    T1 = T; 
  endfor
 
  g = cos((n+1)*acos(x))/2^n;
  plot(x,f,x,g);
  L = max(abs(f))/max(abs(g));
endfunction
