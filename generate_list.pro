PRO GENERATE_LIST

FIND_FLARES, ['2017-04-01 00:00','2017-04-04 00:00'], flares,rad_dist=930, /class

fname='test_dataset_test.dat'
OPENW,1,fname 
for i=0,n_elements(flares)-1 do begin
   x = flares[i].POSITION[0,*]
   y = flares[i].POSITION[1,*]
;if sqrt(x^2 + y^2) GT 930 then begin
   if sqrt(x^2 + y^2) LE 930 then begin
      printf,1,anytim(flares[i].start_time,/stime),anytim(flares[i].end_time,/stime),$
                     x, y, sqrt(x^2+y^2),flares[i].goes_class,$
             FORMAT='(A20,1X,A20,1X,F8.2,1X,F8.2,1X,F8.2,1X,A4)' 
      print,anytim(flares[i].start_time,/stime),anytim(flares[i].end_time,/stime),$
                    x, y, sqrt(x^2+y^2),flares[i].goes_class,$
            FORMAT='(A20,1X,A20,1X,F8.2,1X,F8.2,1X,F8.2,1X,A4)' 
   endif
endfor
CLOSE,1
print,n_elements(flares)
END
