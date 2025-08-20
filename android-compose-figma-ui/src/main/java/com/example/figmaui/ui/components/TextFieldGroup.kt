package com.example.figmaui.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Divider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Text Field Group component based on Figma design
 * Represents a list item with text content in a bordered container
 */
@Composable
fun TextFieldGroup(
    text: String = "MacOS",
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(8.dp))
            .background(Color.White)
            .border(
                width = 1.dp,
                color = Color(0xFFCDD0D6),
                shape = RoundedCornerShape(8.dp)
            )
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        // Frame container
        Column(
            modifier = Modifier.fillMaxWidth()
        ) {
            // List container
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Side Left & Text Item
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Text Item
                    Column(
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            text = text,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF64686E),
                            lineHeight = 24.sp
                        )
                    }
                }
            }
            
            // Bottom border divider
            Divider(
                color = Color(0xFFEBECEE),
                thickness = 1.dp
            )
        }
    }
}
