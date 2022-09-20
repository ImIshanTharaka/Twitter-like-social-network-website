document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#profile_view').style.display = 'none';
  document.querySelector('#following_view').style.display = 'none';
  document.querySelector('#edit_post_form').style.display = 'none';

  if (document.querySelector('#following')){
    document.querySelector('#following').addEventListener('click', following_posts);
  } else {
    document.querySelector('#new_post').onsubmit = function() {
      window.location = "http://127.0.0.1:8000/login";
    }
  }

  // Use buttons to toggle between views
  document.querySelector('#network').addEventListener('click', all_posts);
  document.querySelector('#all_posts').addEventListener('click', all_posts);

  // By default
  all_posts();
});


function all_posts(){
  document.querySelector('#all_posts_view').style.display = 'block';
  document.querySelector('#profile_view').style.display = 'none';
  document.querySelector('#following_view').style.display = 'none';

  // submit new post 
  document.querySelector('#new_post').onsubmit = function () {
    fetch('/new_post', {          //sending a web request to the url and gets a http response back
        method: 'POST',
        body: JSON.stringify({      
          body: document.querySelector('#new_post_body').value
        })
      })
      location.reload()         //reload the page
      return false          //not directing for another url
  }

  // desplay all posts
  fetch (`/show_posts`)
  .then(response => response.json())
  .then(posts => {
    console.log(posts)
    posts.forEach(post => {
      post=create_post(post);
      document.querySelector('#all_posts_view').append(post)
    });
  })
} 


function create_post(post) {
  const post_card = document.createElement('div');
  post_card.className = "p-3 my-3 bg-light";

  // header
  const header =  document.createElement('h5');
  header.innerHTML = post.user
  post_card.append(header);
  header.addEventListener("click", () => show_profile(post.user))

  // edit post
  if (post.edit_status == true) {
    const edit = document.createElement('small');
    edit.setAttribute("Id", "edit")
    edit.innerHTML = "Edit";
    post_card.append(edit);
    edit.addEventListener("click", () => edit_post(post_card, post, edit, body))
  }

  // body
  var body = document.createElement('p');
  body.innerHTML = post.body;
  post_card.append(body);

  // like post
  const heart = document.createElement('div');
  heart.className = 'large-font text-left';
  if (post.liked_status == false){
    heart.innerHTML = `<i class="bi bi-heart"></i>`
  } else {
    heart.innerHTML = `<i class="bi bi-heart-fill"></i>`
  }
  const likes_count = document.createElement('span');
  likes_count.className = 'numb';
  likes_count.innerHTML = ` ${post.likes}`
  heart.append(likes_count)
  post_card.append(heart);
  heart.addEventListener("click", () => like_post(post,heart,likes_count))

  // timestamp
  const timestamp = document.createElement('small');
  timestamp.innerHTML = post.timestamp
  post_card.append(timestamp);
  
  return post_card
}


function edit_post(post_card, post, edit, body){
  const edit_form = document.querySelector('#edit_post_form')
  document.querySelector('#edit_post_text').value = post.body;
  edit_form.style.display = 'block';
  edit.style.display = 'none';    //hide edit button
  body.replaceWith(edit_form);

  // save edited post
  document.querySelector('#edit_post_form').onsubmit = function () {
    fetch('/post_edit', {          //sending a web request to the url and gets a http response back
        method: 'PUT',
        body: JSON.stringify({
          post_id: post.id,       
          body: document.querySelector('#edit_post_text').value
        })
      })
    .then(response => response.json())
    .then(edited_post => {
      edited_post=create_post(edited_post);
      post_card.replaceWith(edited_post);
      document.querySelector('.m-3').append(edit_form)    // edit_form back to initial state
      edit_form.style.display = 'none';
    })
  return false       
  }

}

function like_post(post,heart,likes_count){
  fetch (`like_post/${post.id}`)
  .then(response => response.json())
  .then(data => {
    if (data["new_status"] === false){
      heart.innerHTML = `<i class="bi bi-heart"></i>`
    } else {
      heart.innerHTML = `<i class="bi bi-heart-fill"></i>`
    }
    likes_count.innerHTML = ` ${data["likes_count"]}`;
    heart.append(likes_count)
  });  
}


function show_profile(user_name){
  document.querySelector('#all_posts_view').style.display = 'none';
  document.querySelector('#profile_view').style.display = 'block';
  document.querySelector('#following_view').style.display = 'none';

  // display profile data
  fetch (`profile/${user_name}`)
  .then(response => response.json())
  .then(data => {
      console.log(data)
      if (data["follow_availability"] === false){
        document.querySelector('#follow_button').style.display = 'none';
      }
      
      if (data["following_status"] === true){
        document.querySelector('#follow_button').innerHTML = "Unfollow"
      } else {
        document.querySelector('#follow_button').innerHTML = "Follow"
      }

      document.querySelector('#follow_button').addEventListener('click', () => follow_button(user_name,data));

      document.querySelector('#profile_name').innerHTML = data["user"];
      document.querySelector('#following_count').innerHTML = data["following"];
      document.querySelector('#followers_count').innerHTML = data["followers"];
  })

  // display profile posts
  fetch (`posts/${user_name}`)
  .then(response => response.json())
  .then(posts => {
    posts.forEach(post => {
        post=create_post(post);
        document.querySelector('#profile_view').append(post);
      })
  });
}


function following_posts(){
  document.querySelector('#all_posts_view').style.display = 'none';
  document.querySelector('#profile_view').style.display = 'none';
  document.querySelector('#following_view').style.display = 'block';

  // display following posts
  fetch (`/following_posts`)
  .then(response => response.json())
  .then(posts => {
    console.log(posts)
    posts.forEach(post => {
        post=create_post(post);
        document.querySelector('#following_view').append(post);
      })
  });
}


function follow_button(user_name){
  fetch (`new_follower/${user_name}`)
  .then(response => response.json())
  .then(data => {
    if (data["new_status"] === false){
      document.querySelector('#follow_button').innerHTML = "Follow"; 
    } else {
      document.querySelector('#follow_button').innerHTML = "Unfollow";
    }
    document.querySelector('#followers_count').innerHTML = data["followers_count"];
  });
}


