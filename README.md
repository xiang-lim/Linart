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

---

Note: From this project noticed a few things
1. Depth perception issue: Using an image, it's hard for the computer to determine which sections of the image is
more "in front of" the other .
2. Hard to define which point is on the edge and which are enclosed or excluded by the "edge". Perhaps there are 
other factors needed to be considered to determine the edge.
3. Multi-Processing vs Multi-Threading
    - Multi-Processing: Better for more intense cpu
    - Multi-Threading: Better for IO