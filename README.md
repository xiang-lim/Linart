## Linart

---

### Description

A project that converts jpeg images into a line art

---

### Requirements

1. numpy
2. pandas
3. matplotlib
4. PIL

---

### Status

- In Progress

---

### Journey

#### 1. Converting jpeg images to grayscale

The main purpose for this step is to allow easier computation for HOG.
Using grayscale, the only values lies in the range from 0 to 255.

A function in the Python Imaging Library to do the conversion.

#### 2. Calculate the image gradient

Adapting from Histogram of Oriented Gradient (HOG), each pixel has its
magnitude and orientation calculated by the values of pixels located top,
bottom, left, and right of the said pixel.

`magnitude = ((top pixel - bottom pixel) ** 2 + (right pixel - left pixel)** 2) ** 0.5`

`orientation = atan((top pixel - bottom pixel) / (right pixel - left pixel))`

The resulting array has a length - 2 pixels and width - 2 pixels from the original image.

#### 3. Determine edges

To determine which pixels are indicating the presence of an edge, a threshold is being used.
The pixels that are outliers (above specified threshold) are indicators of an edge.

Here are some tests where outlier points are indicated by
being above 99.7% (3 sigma), 95.4%(2 sigma), 93.5%, 91.6%, 90% of other points

<blockquote>

**Points Plot**

<details>
<summary>99.7%</summary>

![Plot_Point_Attempt_1.png](Attempts%2FAttempt1%2FVariation_1%2FPlot_Point_Attempt_1.png)
</details>

<details>
<summary>95.4%</summary>

![Plot_Point_Attempt_1.png](Attempts%2FAttempt1%2FVariation_2%2FPlot_Point_Attempt_1.png)
</details>

<details>
<summary>93.5%</summary>

![Plot_Point_Attempt_1.png](Attempts%2FAttempt1%2FVariation_3%2FPlot_Point_Attempt_1.png)
</details>

<details>
<summary>91.6%</summary>

![Plot_Point_Attempt_1.png](Attempts%2FAttempt1%2FVariation_4%2FPlot_Point_Attempt_1.png)
</details>

<details>
<summary>90.0%</summary>

![Plot_Point_Attempt_1.png](Attempts%2FAttempt1%2FVariation_5%2FPlot_Point_Attempt_1.png)
</details>
</blockquote>

#### 4. Develop the string art

<blockquote>

**First Approach**

By using each edge points, it is possible to calculate the line equation of the gradient of change
of the image. The assumption for the first approach is to draw the perpendicular for each
respective line calculated.

The results are disappointing...

<details>
<summary>99.7%</summary>

![String_Art_Attempt_1.png](Attempts%2FAttempt1%2FVariation_1%2FString_Art_Attempt_1.png)
</details>

<details>
<summary>95.4%</summary>

![String_Art_Attempt_1.png](Attempts%2FAttempt1%2FVariation_2%2FString_Art_Attempt_1.png)
</details>

<details>
<summary>93.5%</summary>

![String_Art_Attempt_1.png](Attempts%2FAttempt1%2FVariation_3%2FString_Art_Attempt_1.png)
</details>

<details>
<summary>91.6%</summary>

![String_Art_Attempt_1.png](Attempts%2FAttempt1%2FVariation_4%2FString_Art_Attempt_1.png)
</details>

<details>
<summary>90.0%</summary>

![String_Art_Attempt_1.png](Attempts%2FAttempt1%2FVariation_5%2FString_Art_Attempt_1.png)
</details>
</blockquote>

<blockquote>

**Second Approach**

Develop circular points by taking the diagonal length of the image as the diameter. These circular points
will be anchors for the lines representing the points. The places where the lines are tangent to will 
indicate the edge points.

However, this method is disappointing. Each point cannot be represented by a single line that is tangent
to said point.

<details>
<summary>Outcome</summary>

![String_Art_Attempt_2.png](Attempts%2FAttempt2%2FVariation_1%2FString_Art_Attempt_2.png)
</details>

</blockquote>
<blockquote>

**Third Approach**

For this approach, the thought process is to calculate the line weight of each individual line
for n(n-1)/2 combinations, where n is the number of anchors. In this step the line turn into 
individual vectors. The weight of the line is calculated based on the presence of line in the y value.
Because of the heavy computation, 
I had to use multiprocessing library to speed up the task. 

To generate the string art, each string is calculated based on the impact to the resultant image.
However, the process took more than a minute for a line.
</blockquote>

<blockquote>

**Fourth Approach**

The fourth aims to optimize this by utilizing 
`x = pinv(A)b` where A is the matrix of line vector, b is the image vector

<details>
<summary>Outcome</summary>

However, seeing the account, it appears that there might be issues with how
I computed the weight of each string.
![Test.png](Attempts%2FAttempt4%2FTest.png)
</details>
</blockquote>

<blockquote>

**Fifth Approach**

I optimize the calculation of the weight of string by factoring the width of the string. For
each string there are 2 main lines denoting the boundary of the string. If the weight of the 
line on the pixel depends on how much the pixel is being covered. 2 other lines are present 
to calculate the weight of the string shadow.

<details>
<summary>Outcome</summary>

It seems that there is an issues in selecting the next possible line
<details>
<summary>Part 1:</summary>

![0.png](Attempts%2FAttempt5%2F0.png)
</details>

<details>
<summary>Part 2:</summary>

![1.png](Attempts%2FAttempt5%2F1.png)
</details>

<details>
<summary>Part 3:</summary>

![2.png](Attempts%2FAttempt5%2F2.png)
</details>

<details>
<summary>Part 4:</summary>

![3.png](Attempts%2FAttempt5%2F3.png)
</details>

<details>
<summary>Part 5:</summary>

![4.png](Attempts%2FAttempt5%2F4.png)
</details>

<details>
<summary>Part 6:</summary>

![5.png](Attempts%2FAttempt5%2F5.png)
</details>

<details>
<summary>Part 7:</summary>

![6.png](Attempts%2FAttempt5%2F6.png)
</details>

</details>
</blockquote>

<blockquote>

**Sixth Approach**

To optimize the selection of the best possible line with greedy algorithm and 
`min
x
​
∣∣Ax−b∣∣**2`

The first attempt was to use `np.linalg.norm(A.dot(x) - b)**2` to calculate 
the error.

However, doing a dot product on a matrix that is size 2556 X 409600 is not a good idea. 
This solution consumes massive amount of memory. 

In an attempt to resolve this `x = np.dot(np.linalg.pinv(A), image_vector)` was used. 
The initial idea was to determine the line by getting the largest x values. But
PseudoInverse of A returns a range of values that include < 0.

<details>
<summary>Attempt 6</summary>

The image the program is trying to create is a hollow circle.

![circle_12.png](Attempts%2FAttempt6%2Fcircle_12.png)
</details>

To reduce the memory usage of `np.linalg.norm(A.dot(x) - b)**2`, I calculate the norm
difference between line vector and the image vector. The best line chosen is the line where
the norm is smallest.

With a bit of tweaking of the string weights and the image weights the image is clearer.

<details>
<summary>Attempt 7</summary>

This is the 13th image generated.

![circle_13.png](Attempts%2FAttempt7%2Fcircle_13.png)

<details>
<summary> Process of image generated </summary>

![circle_1.png](Attempts%2FAttempt7%2Fcircle_1.png)
![circle_2.png](Attempts%2FAttempt7%2Fcircle_2.png)
![circle_3.png](Attempts%2FAttempt7%2Fcircle_3.png)
![circle_4.png](Attempts%2FAttempt7%2Fcircle_4.png)
![circle_5.png](Attempts%2FAttempt7%2Fcircle_5.png)
![circle_6.png](Attempts%2FAttempt7%2Fcircle_6.png)
![circle_7.png](Attempts%2FAttempt7%2Fcircle_7.png)
![circle_8.png](Attempts%2FAttempt7%2Fcircle_8.png)
![circle_9.png](Attempts%2FAttempt7%2Fcircle_9.png)
![circle_10.png](Attempts%2FAttempt7%2Fcircle_10.png)
![circle_11.png](Attempts%2FAttempt7%2Fcircle_11.png)
![circle_12.png](Attempts%2FAttempt7%2Fcircle_12.png)
![circle_13.png](Attempts%2FAttempt7%2Fcircle_13.png)
![circle_14.png](Attempts%2FAttempt7%2Fcircle_14.png)
![circle_final.png](Attempts%2FAttempt7%2Fcircle_final.png)
</details>
</details>
</blockquote>

<blockquote>

**Cherry-Picked images generated from this program**

<details>
<summary>Circle</summary>

![circle_13.png](Attempts%2FAttempt7%2Fcircle_13.png)
</details>
</blockquote>

---

Note: From this project noticed a few things
1. Depth perception issue: Using an image, it's hard for the computer to determine which sections of the image is
more "in front of" the other .
2. Hard to define which point is on the edge and which are enclosed or excluded by the "edge". Perhaps there are 
other factors needed to be considered to determine the edge.
3. Multi-Processing vs Multi-Threading
    - Multi-Processing: Better for more intense cpu
    - Multi-Threading: Better for IO