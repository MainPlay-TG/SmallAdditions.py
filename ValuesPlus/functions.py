SECOND=1
MILLISECOND=SECOND/1000
MICROSECOND=MILLISECOND/1000
NANOSECOND=MICROSECOND/1000
MINUTE=SECOND*60
HOUR=MINUTE*60
DAY=HOUR*24
WEEK=DAY*7
YEAR=DAY*365
CENTURY=YEAR*100

BYTE=1
KILOBYTE=BYTE*1024
MEGABYTE=KILOBYTE*1024
GIGABYTE=MEGABYTE*1024
TERABYTE=GIGABYTE*1024
PETABYTE=TERABYTE*1024
EXAPYTE=PETABYTE*1024
ZETTABYTE=EXABYTE*1024

BIT=BYTE/8
KILOBIT=BIT*1024
MEGABIT=KILOBIT*1024
GIGABIT=MEGABIT*1024
TERABIT=GIGABIT*1024
PETABIT=TERABIT*1024
EXAPYTE=PETABIT*1024
ZETTABIT=EXABIT*1024

time={}
for k,v in locals().items():
  if k in ["NANOSECOND","MICROSECOND","MILLISECOND","SECOND","MINUTE","HOUR","DAY","WEEK","YEAR","CENTURY"]:
    time[k]=v
size={}
for k,v in locals().items():
  if k in ["BIT","BYTE","KILOBIT","KILOBYTE","MEGABIT","MEGABYTE","GIGABIT","GIGABYTE","TERABIT","TERABYTE","PETABIT","PETABYTE","EXAPYTE","EXAPYTE","ZETTABIT","ZETTABYTE"]:
    size[k]=v
class duration:
  def __init__(self,nanoseconds=0,microseconds=0,milliseconds=0,seconds=0,minutes=0,hours=0,days=0,weeks=0,years=0)
    self._names={
      "nanoseconds":NANOSECOND,
      "microseconds":MICROSECOND,
      "milliseconds":MILLISECOND,
      "seconds":SECOND,
      "minutes":MINUTE,
      "hours":HOUR,
      "days":DAY,
      "weeks":WEEK,
      "years":YEAR,
      }
    values=locals()
    for k in self._names.keys():
      setattr(self,k,values[k])
  def _units2total(self):
    self.total_seconds=0.0
    for k,v in self._names.items():
      self.total_seconds+=getattr(self,k)*v
  def _total2units(self):
    pass