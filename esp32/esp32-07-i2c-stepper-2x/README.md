# 2x stepp motor basic test
<code>
...
int vel = 10;
for(int i=0;i<8;i++)
  {
  down((6-i)*vel);
  left((6-i)*vel);
  up((6-i)*vel);
  right((6-i)*vel); 
  }  
</code>
