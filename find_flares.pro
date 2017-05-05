PRO FIND_FLARES, time_range, flares, rad_dist = rad_dist, class = class
; Calculate which rhessi flares fit the standards

  ; INPUTS
  ;    time_range : overall time range in which to look for flares
  ;    rad_dist   : max radial distance
  ;    class      : if set, return only flares of C class or higher

  ; OUTPUTS
  ;    flares  : flarelist of chosen flares


  if not keyword_set(rad_dist)  then rad_dist  = 0. ;maximum distance above solar limb

  ; Get all flares in given time range
  flare_list_obj =  hsi_flare_list(obs_time_interval =  anytim(time_range, /ecs))
  flare_list =  flare_list_obj -> getdata()
  nFlaresTot =  n_elements(flare_list)

  if nFlaresTot eq 0 or size(flare_list, /type) eq 2 then begin
    print, 'No flares found in this time range.'
    return
 endif

  x = flare_list.position[0,*]
  y = flare_list.position[1,*]

  ; cut list down to flares above limb + rad_dist

  ; note that if get_rb0p doesn't work, pb0r sometimes does.
  start_time = anytim(flare_list.start_time, /ecs)
;  print, start_time
  rad = get_rb0p(start_time) ;get solar radius at time of flare
  index = where( sqrt(x^2+y^2) le (rad_dist), count)

  print, nFlaresTot, ' total flares in time period.'
  print, count, ' flares matching cuts.'

  if count eq 0 then return ;return if no flares are found.

  flare_list_cut = flare_list[index]

  if keyword_set(class) then begin
      class = string(flare_list_cut.goes_class)
      bb = where(strmid(class, 0, 1) eq 'B', n_bb)
      cc = where(strmid(class, 0, 1) eq 'C', n_cc)
      mm = where(strmid(class, 0, 1) eq 'M', n_mm)
      xx = where(strmid(class, 0, 1) eq 'X', n_xx)
      list = [cc, mm, xx]
      i = where(list eq -1)
      if i[0] ne -1 then remove, i, list
      flare_list_cut = flare_list_cut[list]
      print, n_elements(list), ' flares of appropriate goes class.'
   endif

  ;define output parameters
  flares = flare_list_cut
  print,n_elements(flares)
  ;tPeaks  = flare_list_cut.peak_time
  ;pos = flare_list_cut.position
  ;ID = flare_list_cut.id_number
  ;start = flare_list_cut.start_time

END
