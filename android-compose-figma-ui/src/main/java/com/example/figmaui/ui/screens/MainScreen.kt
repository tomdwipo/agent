package com.example.figmaui.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.figmaui.ui.components.TextFieldGroup

/**
 * Main screen showcasing the TextFieldGroup component
 * Based on the Figma design data
 */
@Composable
fun MainScreen(
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp)
        ) {
            // Sample data based on Figma design
            val sampleItems = listOf(
                "MacOS",
                "Windows",
                "Linux",
                "Android",
                "iOS"
            )
            
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(sampleItems) { item ->
                    TextFieldGroup(text = item)
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun MainScreenPreview() {
    MaterialTheme {
        MainScreen()
    }
}
