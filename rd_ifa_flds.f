      program rd_ifa_flds 
c
c   sample routine to read in ifa averaged fields
c
c   f77 rd_ifa_flds.f -o rd_ifa_flds.x  -L/usr/remote/lib -lplotf
c
      parameter (npds = 480, kk=41 )       

      parameter (xmis = -999.)

c   bt - satellite brightness temperature (C)
c   sst - sea surface temperature (C)
c   so  - surface sensible heat flux (mm/day)
c   eo  - surface latent heat flux (mm/day)
c   po  - budget-derived rainfall rate (mm/day)
c   qr  - budget-derived net radiative heating rate (K/day)
c   z   - height 
c   u   - zonal-wind component
c   v   - meridional-wind component
c   q   - specific humidity (g/kg)
c   rh  - relative humidity (%)
c   pr  - pressure (hPa)
c   div  - horizontal divergence (1/s)*10^6
c   w  -  omega (mb/hr)
c   q1  -  apparent heating (K/day) 
c   q2  -  apparent drying (K/day) 
c   ht  -  horizontal advection of T (K/s) 
c   vt  -  vertical  advection of T (K/s) 
c   hq  -  horizontal advection of q ((g of vapor/g of air)/s) 
c   vq  -  vertical  advection of q ((g of vapor/g of air)/s)) 
c
      real bt(npds), sst(npds), so(npds), eo(npds), po(npds), qr(npds) 
      real z(npds,kk), t(npds,kk), q(npds,kk), rh(npds,kk)
      real u(npds,kk), v(npds,kk), div(npds,kk), w(npds,kk)
      real pr(kk), q1(npds,kk), q2(npds,kk)
      real ht(npds,kk), vt(npds,kk), hq(npds,kk), vq(npds,kk)

      integer iy, im, id, ih                        

c   *************************************************************************

c  f2 - factor to go from mm/day to watts/(m*m)
c  f3 - factor to go from mm/day to K/day 

      lv = 2.5e6
      f2 = lv / (3.6e3 * 24.)
      f3  = f2/108.

c   open files for input

      open(27, file='basic_flds.ifa', status='old')
      open(28, file='deriv_flds.ifa', status='old')
      open(29, file='misc_flds.ifa',  status='old')
      open(30, file='lsf_flds.ifa',   status='old')


      np = 0
      nq = 0
      posum = 0.
      qrsum = 0.
      do ip=1,npds
         read(27,223) iy, im, id, ih              
         read(28,223) iy, im, id, ih              
         read(29,223) iy, im, id, ih, bt(ip), sst(ip), so(ip), 
     2                 eo(ip), po(ip), qr(ip)
         read(30,223) iy, im, id, ih             

         if (po(ip) .ne. xmis) then
            np = np + 1
            posum = posum + po(ip)
         endif
         if (qr(ip) .ne. xmis) then
            nq = nq + 1
            qrsum = qrsum + qr(ip)
         endif

         do  k=1,kk
            read(27,226) pr(k), z(ip,k), t(ip,k), q(ip,k), 
     2                          rh(ip,k), u(ip,k), v(ip,k)
            read(28,226) pr(k), div(ip,k), w(ip,k), q1(ip,k), q2(ip,k)
            read(30,227) pr(k), ht(ip,k), vt(ip,k), hq(ip,k), vq(ip,k) 
         enddo
      enddo

      print *, 'average rainfall (mm/day) ', posum/float(np)
      print *, 'average qrnet (K/day) ', qrsum/float(nq)*f3


  223 format(4i3,6f8.2)
  226 format(f7.1,1x,10f8.2)
  227 format(f7.1,1x,1p,4e11.3)

      end
