CREATE TABLE profiles (
    profile_id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    name TEXT NOT NULL,
    interests TEXT,
    birthday DATE,
    start_date DATE NOT NULL
);

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    profile_id INT NOT NULL,  -- Foreign key from profiles table
    post_content TEXT NOT NULL,
    post_date DATE NOT NULL,
    likes INT
);

CREATE TABLE images (
    image_id SERIAL PRIMARY KEY,
    image_url TEXT NOT NULL UNIQUE,
    upload_date DATE NOT NULL,
    post_id INT  -- Foreign key from posts table
);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    image_id INT,  -- Foreign key from image table
    post_id INT,     -- Foreign key from posts table
    comment_content TEXT NOT NULL,
    comment_date DATE NOT NULL
);

---  I wanted to create 4 relationships; 
--------------one between profile and posts,
--------------posts and images, 
--------------posts and comments, 
--------------and comments and images


-- Add foreign key from posts table to profiles table
ALTER TABLE posts
ADD CONSTRAINT fk_posts_profiles
FOREIGN KEY (profile_id)
REFERENCES profiles(profile_id);

-- Add foreign key from images table to posts table
ALTER TABLE images
ADD CONSTRAINT fk_images_posts
FOREIGN KEY (post_id)
REFERENCES posts(post_id);

-- Add foreign key from comments table to posts table
ALTER TABLE comments
ADD CONSTRAINT fk_comments_posts
FOREIGN KEY (post_id)
REFERENCES posts(post_id);

-- Add foreign key from comments table to images table
ALTER TABLE comments
ADD CONSTRAINT fk_comments_images
FOREIGN KEY (image_id)
REFERENCES images(image_id);

INSERT INTO profiles (username, password, name, interests, birthday, start_date)
VALUES ('user1', 'password1', 'Demo Guy', 'Sports, Music', '1995-04-10', '2020-01-01'),
('user2', 'password2', 'Demo Girl', 'Art, Travel', '1990-04-10', '2020-02-01');

INSERT INTO posts (profile_id, post_content, post_date, likes)
VALUES (1, 'First Post and Two Pictures', '2024-05-01', 10), 
(2, 'Second Post and no Picture', '2024-05-02', 5);

INSERT INTO images (image_url, upload_date, post_id)
VALUES ('image1.com', '2024-05-01', 1),
('image2.com', '2024-05-02', NULL), 
('image3.com', '2024-05-02', NULL), 
('image4.com', '2024-05-03', NULL);

INSERT INTO comments (image_id, post_id, comment_content, comment_date)
VALUES (1, 1, 'Great picture', '2024-05-01'),
(2, NULL, 'Wow', '2024-05-01'),
(3, NULL, 'Cool', '2024-05-02'),
(4, 1, 'Neat first post', '2024-05-02');

