# what's a mask?
a "mask" in this situation is an html file (could be literally anything actually) with a specific html comment tag  

the comment tag in question is this:
```
<!--%()%-->
```

the hoaxshell manager will automatically replace ``%()%`` with the encoded command, for the victim to parse it  

# where do i get a mask?
literally anywhere

a good way of making some is:

1. open the site you want to turn into a mask
2. right click -> view source (for firefox, idk about others)
3. copy and paste everything into a new file under ./core/masks/html/ (ex: google.html)
4. paste it in that file, find somewhere to make a comment, paste the tag
5. profit 😸

so a mask could literally just be

```
<!DOCTYPE html>
<html>
<body>

<h1>My First Heading</h1>

<p>My first paragraph.</p>

<!--%()%-->   < heres the comment tag

</body>
</html>
```

the payload will automatically figure out which comment is correct (usually), so you can go crazy with the masks  
yes, that also means you can make pornhub a mask

enjoy 😸
